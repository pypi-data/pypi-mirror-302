// Cytosim was created by Francois Nedelec. Copyright 2007-2017 EMBL.

#include "interface.h"
#include "stream_func.h"
#include "exceptions.h"
#include "simul_prop.h"
#include "tokenizer.h"
#include "evaluator.h"
#include "messages.h"
#include "glossary.h"
#include "filepath.h"
#include "tictoc.h"
#include "simul.h"
#include "event.h"
#include "sim.h"
#include <fstream>


// Use the second definition to get some verbose reports:
#define VLOG(ARG) ((void) 0)
//#define VLOG(ARG) std::clog << ARG;

//------------------------------------------------------------------------------

Interface::Interface(Simul& s)
: simul(s)
{
}

//------------------------------------------------------------------------------
#pragma mark -


/**
 This creates a new Property
 
 Property::complete() is called after a property is set.
 This ensures that inconsistencies are detected as early as possible.
 
 The drawback is that we cannot support cross-dependencies (A needs B and vice-versa).
 If that is necessary, we could:
 - call complete() for all Properties, after the parsing process is complete.
 - remove any check for the existence of invoked properties, in which case 
 error would be detected only when objects are created later.
 */
Property* Interface::execute_set(std::string const& cat, std::string const& name, Glossary& def)
{
    VLOG("+SET " << cat << " `" << name << "'\n");
    
    /* We do not allow for using the class name to name a property,
    as this should create confusion in the config file */
    
    Property* pp = simul.newProperty(cat, name, def);
    
    if ( !pp )
        throw InvalidSyntax("failed to create property of class `"+cat+"'");
    
    pp->read(def);
    pp->complete(simul);
    
    return pp;
}


void Interface::execute_change(Property * pp, Glossary& def)
{
    pp->read(def);
    pp->complete(simul);
    
    /*
     Specific code to make 'change space:dimension' work.
     This is needed as dimensions are specified in Space hold, and not SpaceProp
     */
    if ( pp->category() == "space" )
    {
        // update any Space with this property:
        for ( Space * s = simul.spaces.first(); s; s=s->next() )
        {
            if ( s->prop == pp )
            {
                s->resize(def);
                // allow Simul to update periodic:
                if ( s == simul.spaces.master() )
                    simul.spaces.setMaster(s);
            }
        }
    }
}


// in this form, 'name' designates the property name
Property * Interface::execute_change(std::string const& name, Glossary& def, bool strict)
{
    Property * pp = simul.findProperty(name);
    
    if ( pp )
    {
        VLOG("-CHANGE " << pp->category() << " `" << name << "'\n");
        execute_change(pp, def);
    }
    else
    {
        if ( strict )
            throw InvalidSyntax("unknown property `"+name+"'");
        else
        {
            VLOG("unknown change |" << name << "|\n");
        }
    }
    return pp;
}


void Interface::execute_change_all(std::string const& cat, Glossary& def)
{
    PropertyList plist = simul.findAllProperties(cat);
    
    for ( Property * i : plist )
    {
        VLOG("+CHANGE " << i->category() << " `" << i->name() << "'\n");
        execute_change(i, def);
    }
}


//------------------------------------------------------------------------------
#pragma mark -

/// report warning
void warn_trail(std::istream& is, std::string const& msg)
{
    std::string str;
    std::streampos pos = is.tellg();
    std::getline(is, str);
    throw InvalidSyntax("unexpected `"+str+"' in `"+StreamFunc::get_line(is, pos)+"'");
}

/**
 Define a placement = ( position, orientation ) from the parameters set in `opt'
 */
Isometry Interface::read_placement(Glossary& opt)
{
    Isometry iso;
    std::string str;
    
    Space const* spc = simul.spaces.master();
    
    // Space specified as second argument to 'position'
    if ( opt.set(str, "position", 1) )
        spc = simul.findSpace(str);
    
    // Position
    if ( opt.set(str, "position") )
    {
        std::istringstream iss(str);
        iso.mov = Movable::readPosition(iss, spc);
        if ( StreamFunc::has_trail(iss) ) warn_trail(iss, "position = "+str);
    }
    else if ( spc )
    {
        iso.mov = spc->randomPlace();
    }
    
    // Rotation applied before the translation
    if ( opt.set(str, "orientation") )
    {
        std::istringstream iss(str);
        iso.rot = Movable::readOrientation(iss, iso.mov, spc);
        if ( StreamFunc::has_trail(iss) ) warn_trail(iss, "orientation = "+str);
    }
    else if ( opt.set(str, "direction") )
    {
        std::istringstream iss(str);
        Vector vec = Movable::readDirection(iss, iso.mov, spc);
        if ( StreamFunc::has_trail(iss) ) warn_trail(iss, "direction = "+str);
        iso.rot = Rotation::randomRotationToVector(vec);
    }
    else
        iso.rot = Rotation::randomRotation();
    
    // Second rotation applied after the translation
    if ( opt.set(str, "orientation", 1) )
    {
        std::istringstream iss(str);
        Rotation rot = Movable::readOrientation(iss, iso.mov, spc);
        if ( StreamFunc::has_trail(iss) ) warn_trail(iss, "orientation = "+str);
        iso.rotate(rot);
    }
    
    return iso;
}


enum PlacementType { PLACE_NOT, PLACE_ANYWHERE, PLACE_INSIDE, PLACE_EDGE,
                     PLACE_OUTSIDE, PLACE_ALL_INSIDE };


/**
 
     new INTEGER CLASS NAME
     {
       position = POSITION
       placement = PLACEMENT, SPACE_NAME, CONDITION
       nb_trials = INTEGER
     }
 
 PLACEMENT can be:
 - if placement = `inside` (default), it tries to find a place inside the Space
 - if placement = `anywhere`, the position is returned
 - if placement = `outside`, the object is created only if it is outside the Space
 - if placement = `surface`, the position is projected on the edge of current Space
 .
 
 By default, the specifications are relative to the first Space to be defined,
 but a different space can be specified as second argument of PLACEMENT.
 
 You can set the density of objects with `nb_trials=1`:
 
     new 100 grafted
     {
       position = ( rectangle 10 10 )
       nb_trials = 1
     }
 
 In this way an object will be created only if its randomly chosen position falls
 inside the Space, and the density will thus be exactly what is specified from the
 `position` range (here 100/10*10 = 1 object per squared micrometer).
 */
bool Interface::find_placement(Isometry& iso, Glossary& opt, int placement)
{
    std::string str;
    Space const* spc = simul.spaces.master();
    if ( opt.set(str, "placement", 1) )
        spc = simul.findSpace(str);

    // generate a new position:
    iso = read_placement(opt);
    
    if ( iso.invalid() )
        return 0;
    
    // check any conditions to the position:
    bool has_condition = opt.set(str, "placement", 2);
    if ( has_condition )
    {
        Evaluator evaluator{{'X', iso.mov.x()}, {'Y', iso.mov.y()}, {'Z', iso.mov.z()},
            {'R', iso.mov.norm()}, {'P', RNG.preal()}};
        try {
            if ( 0 == evaluator.evaluate(str.c_str()) )
                return 0;
        }
        catch( Exception& e ) {
            e.message(e.message()+" in `"+str+"'");
            throw;
        }
    }
    
    if ( !spc || placement == PLACE_ANYWHERE )
        return 1;
    
    if ( placement == PLACE_EDGE )
    {
        iso.mov = spc->project(iso.mov);
        return 1;
    }
    
    if ( spc->inside(iso.mov) )
    {
        if ( placement == PLACE_INSIDE || placement == PLACE_ALL_INSIDE )
            return 1;
    }
    else
    {
        if ( placement == PLACE_OUTSIDE )
            return 1;
    }
    
    return 0;
}



bool all_points_inside(ObjectList const& objs, Space const* spc)
{
    for ( Object * i : objs )
    {
        Mecable * mec = Simul::toMecable(i);
        if ( mec && ! mec->allInside(spc) )
            return false;
    }
    return true;
}

/**
 This would usually create ONE object of type 'pp', placed according to `opt`
 */
ObjectList Interface::new_object(ObjectSet* set, Property const* pp, Glossary& opt)
{
    ObjectList objs;
    long max_trials = 1024;
    opt.set(max_trials, "nb_trials");
    long nb_trials = max_trials;
    Glossary::dict_type<PlacementType> keys{
        {"off",        PLACE_NOT},
        {"none",       PLACE_NOT},
        {"anywhere",   PLACE_ANYWHERE},
        {"inside",     PLACE_INSIDE},
        {"all_inside", PLACE_ALL_INSIDE},
        {"outside",    PLACE_OUTSIDE},
        {"surface",    PLACE_EDGE}};
    
    while ( --nb_trials >= 0 )
    {
        objs = set->newObjects(pp->name(), opt);
        
        // early bailout for immobile objects:
        if ( objs.size()==1 && !objs[0]->mobile() )
            break;
        
        PlacementType placement = PLACE_INSIDE;
        opt.set(placement, "placement", keys);
        if ( placement == PLACE_NOT )
            break;
        
        // find possible position & rotation:
        Isometry iso;
        if ( find_placement(iso, opt, placement) )
        {
            // place object at this position:
            for ( Object * obj : objs )
                obj->move(iso);
            // special case for which we check all vertices:
            bool okay = true;
            if ( placement == PLACE_ALL_INSIDE )
            {
                std::string str;
                Space const* spc = simul.spaces.master();
                if ( opt.set(str, "placement", 1) )
                    spc = simul.findSpace(str);
                okay = all_points_inside(objs, spc);
            }
            if ( okay )
                break;
        }
        else
        {
            // no suitable placement found, delete new objects:
            for ( Object* i : objs )
                if ( ! i->linked() )
                    delete(i);
            objs.clear();
            continue;
        }
        /*
         objects that were just created by newObjects() are not yet linked and
         will be deleted. Older objects will be moved back to their original position
         */
        iso.inverse();
        for ( Object* i : objs )
        {
            if ( ! i->linked() )
                delete(i);
            else
                i->move(iso);
        }
        objs.clear();
    }
    
    if ( objs.empty() )
    {
        std::string name = pp ? pp->name() : "object";
        if ( max_trials > 1 )
            Cytosim::log << "could not place `" << name << "' after " << max_trials << " trials\n";
        return objs;
    }

    // optionally mark the objects:
    ObjectMark mk = 0;
    if ( opt.value_is("mark", 0, "random") )
        mk = RNG.pint32();
    if ( mk || opt.set(mk, "mark") )
    {
        for ( Object * i : objs )
            i->mark(mk);
    }

    // translation after placement
    Vector vec;
    if ( opt.set(vec, "translation") )
        ObjectSet::translateObjects(objs, vec);
    
    //std::clog << "new_object " << objs.size() << " " << pp->name() << "\n";
    return objs;
}


/**
 Create `cnt` objects of type 'name', according to specifications.
 It is possible to make an object without an associated Property
 */
ObjectList Interface::execute_new(std::string const& cat, std::string const& name, Glossary& opt, size_t cnt)
{
    ObjectList res;
    ObjectSet * set = nullptr;
    Property const* pp = simul.properties.find(name);
    
    if ( cat.empty() && pp )
    {
        set = simul.findSet(pp->category());
        if ( !set )
            throw InvalidSyntax("could not determine the class of `"+name+"'");
    }
    else if ( cat.empty() )
        throw InvalidSyntax("could not determine the class of `"+name+"'");
    else
    {
        set = simul.findSet(cat);
        if ( !set )
            throw InvalidSyntax("undefined class `"+cat+"'");
    }
    
    size_t amount = set->size();

    // syntax sugar: distribute objects regularly between two points
    if ( opt.has_key("range") )
    {
        Vector A, B;
        if ( !opt.set(A, "range") || !opt.set(B, "range", 1) )
            throw InvalidParameter("two vectors need to be defined by `range'");
        if ( opt.has_key("position") )
            throw InvalidParameter("cannot specify `position' if `range' is defined");
        Vector dAB = ( B - A ) / std::max(1UL, cnt-1);
        
        for ( size_t n = 0; n < cnt; ++n )
        {
            opt.define("position", A + n * dAB);
            res.append(new_object(set, pp, opt));
        }
    }
    // syntax sugar: positions specified for multiple objects
    else if ( opt.nb_values("positions") > 0 )
    {
        for ( size_t n = 0; n < cnt; ++n )
        {
            size_t i = opt.least_used_index(opt.values("positions"));
            opt.define("position", opt.value("positions", i));
            res.append(new_object(set, pp, opt));
        }
    }
    else
    {
        // syntax sugar: specify the positions of the Fiber's ends
        if ( opt.has_key("position_ends") )
        {
            Vector A, B;
            if ( !opt.set(A, "position_ends") || !opt.set(B, "position_ends", 1) )
                throw InvalidParameter("two vectors need to be defined by `position_ends'");
            opt.define("length",    (A-B).norm());
            opt.define("position",  (A+B)*0.5);
            opt.define("direction", (B-A).normalized());
        }
        
        // normal pathway:
        for ( size_t n = 0; n < cnt; ++n )
            res.append(new_object(set, pp, opt));
    }
    //hold();
    
    /*
     Because the objects in ObjectList are not necessarily all of the same class,
     for example a Single can be created along with a Fiber in FiberSet::newObjects,
     we call here sim_->add() rather than directly set->add()
     */
    simul.add(res);

    size_t required = 0;
    if ( opt.set(required, "required") )
    {
        size_t created = set->size() - amount;
        if ( created < required )
        {
            std::cerr << "created  = " << created << '\n';
            std::cerr << "required = " << required << '\n';
            throw InvalidParameter("could not create enough `"+name+"'");
        }
    }

    VLOG("+NEW " << cat << " `" << name << "' made " << set->size()-amount << " objects (total " << sim_->nbObjects() << ")");
    return res;
}


//------------------------------------------------------------------------------
/**
 Creates `cnt` objects of class `name`.
 The objects are distributed at the specified position in the given Space,
 with random orientations.
 
 This is meant to replace execute_new(cat, name, opt, cnt), when no fancy
 option were specified to the command.
 */
ObjectList Interface::execute_new(std::string const& name, size_t cnt,
                                  Space const* spc, std::string const& position)
{
    Property const* pp = simul.properties.find_or_die(name);
    ObjectSet * set = simul.findSet(pp->category());
    if ( !set )
        throw InvalidSyntax("could not determine the class of `"+name+"'");

    Glossary opt;
    ObjectList res;

    for ( size_t n = 0; n < cnt; ++n )
    {
        ObjectList objs = set->newObjects(pp->name(), opt);
        
        if ( objs.empty() )
            throw InvalidSyntax("could not create any `"+name+"'");
        
        Object * obj = nullptr;
        if ( objs.size() == 1 )
            obj = objs[0];

        if ( spc )
        {
            Vector pos;
            if ( position.empty() )
                pos = spc->randomPlace();
            else
                pos = Movable::readPosition(position, spc);
            
            if ( !pos.valid() )
            {
                objs.destroy();
                continue;
            }
            
            if ( obj )
            {
                // here the random rotation is only generated if needed:
                switch ( obj->mobile() )
                {
                    case 2: obj->rotate(Rotation::randomRotation()); break;
                    case 3: obj->rotate(Rotation::randomRotation());
                    case 1: obj->translate(pos);
                }
            }
            else
            {
                Isometry iso(Rotation::randomRotation(), pos);
                for ( Object * o : objs )
                    o->move(iso);
            }
        }
        
        /* Call sim_->add(), in case the list might contain heterogenous objects */
        if ( obj ) {
            set->add(obj);
            res.push_back(obj);
        } else {
            simul.add(objs);
            res.append(objs);
        }
    }
    
    VLOG("-NEW " << cnt << " `" << name << "' at `" << position << "'");
    //hold();
    return res;
}


//------------------------------------------------------------------------------
#pragma mark -

/// holds a set of criteria used to select Objects
class Filter
{
public:

    Space const* ins;
    Space const* ous;
    Property const* prp;
    ObjectMark mrk;
    unsigned st1;
    unsigned st2;

    /// initialize
    Filter()
    {
        mrk = 0;
        st1 = ~0U;
        st2 = ~0U;
        prp = nullptr;
        ins = nullptr;
        ous = nullptr;
    }
    
    void set(Simul& sim, Property* pp, Glossary& opt)
    {
        prp = pp;
        
        std::string str;
        if ( opt.set(str, "position", 1) )
        {
            Space const* spc = sim.spaces.master();
            spc = sim.findSpace(str);
            if ( !spc )
                throw InvalidSyntax("unknown Space `"+str+"'");
            opt.set(str, "position");
            if ( str == "inside" )
                ins = spc;
            else if ( str == "outside" )
                ous = spc;
        }
        
        opt.set(mrk, "mark");
        opt.set(st1, "state1") || opt.set(st1, "stateP") || opt.set(st1, "state");
        opt.set(st2, "state2") || opt.set(st2, "stateM") || opt.set(st1, "state", 1);
    }
    
    /// return `true` if given object fulfills all the conditions specified
    bool pass(Object const* obj) const
    {
        if ( mrk > 0 && obj->mark() != mrk )
            return false;
        if ( ins && ins->outside(obj->position()) )
            return false;
        if ( ous && ous->inside(obj->position()) )
            return false;
        if ( prp && obj->property() != prp )
            return false;
        if ( st1 != ~0U )
        {
            if ( obj->tag()==Single::TAG && static_cast<Single const*>(obj)->attached() != st1 )
                return false;
            if ( obj->tag()==Couple::TAG && static_cast<Couple const*>(obj)->attached1() != st1 )
                return false;
            if ( obj->tag()==Fiber::TAG && static_cast<Fiber const*>(obj)->dynamicStateP() != st1 )
                return false;
        }
        if ( st2 != ~0U )
        {
            if ( obj->tag()==Single::TAG )
                throw InvalidParameter("to select Single, `state2' is irrelevant");
            if ( obj->tag()==Couple::TAG && static_cast<Couple const*>(obj)->attached2() != st2 )
                return false;
            if ( obj->tag()==Fiber::TAG && static_cast<Fiber const*>(obj)->dynamicStateM() != st2 )
                return false;
        }
        return true;
    }
};


bool pass_filter(Object const* obj, void const* val)
{
    return static_cast<Filter const*>(val)->pass(obj);
}


void Interface::execute_delete(std::string const& name, Glossary& opt, unsigned cnt)
{
    Property * pp = simul.properties.find(name);
    ObjectSet * set = nullptr;
    if ( pp )
        set = simul.findSet(pp->category());
    else
        set = simul.findSet(name);
    if ( !set )
    {
        if ( name == "objects" )
        {
            simul.erase();     // deletes everything
            return;
        }
        throw InvalidSyntax("could not determine the class of `"+name+"'");
    }
    
    Filter filter;
    filter.set(simul, pp, opt);
    ObjectList objs = set->collect(pass_filter, &filter);
    
    if ( objs.size() == 0 )
    {
        std::cerr << "Warning: found no `" << name << "' to delete\n";
        return;
    }
    
    if ( cnt == 1 )
    {
        simul.erase(objs.pick_one());
    }
    else
    {
        // optionally limit the list to a random subset
        if ( cnt < objs.size() )
        {
            objs.shuffle();
            objs.truncate(cnt);
        }
        
        //std::clog << "simul:deleting " << objs.size() << " " << set->title() << '\n';
        simul.erase(objs);
    }
}


/**
 This moves objects to position `pos`
 */
void Interface::execute_move(std::string const& name, Glossary& opt, size_t cnt)
{
    Property * pp = simul.properties.find(name);
    ObjectSet * set = nullptr;
    if ( pp )
        set = simul.findSet(pp->category());
    else
        set = simul.findSet(name);
    if ( !set )
        throw InvalidSyntax("could not determine the class of `"+name+"'");
    
    Filter filter;
    filter.set(simul, pp, opt);
    ObjectList objs = set->collect(pass_filter, &filter);
    
    // optionally limit the list to a random subset
    if ( cnt < objs.size() )
    {
        objs.shuffle();
        objs.truncate(cnt);
    }
    
    Vector pos;
    if ( opt.set(pos, "position") )
    {
        for ( Object * obj : objs )
            obj->setPosition(pos);
    }
    else if ( opt.set(pos, "translation") )
    {
        for ( Object * obj : objs )
            obj->translate(pos);
    }
}


void Interface::execute_mark(std::string const& name, Glossary& opt, unsigned cnt)
{
    Property * pp = simul.properties.find(name);
    ObjectSet * set = nullptr;
    if ( pp )
        set = simul.findSet(pp->category());
    else
        set = simul.findSet(name);
    if ( !set )
        throw InvalidSyntax("could not determine the class of `"+name+"'");

    ObjectMark mrk;
    if ( ! opt.set(mrk, "mark") )
        throw InvalidParameter("mark must be specified for command `mark'");
    opt.clear("mark");
    
    Filter filter;
    filter.set(simul, pp, opt);
    ObjectList objs = set->collect(pass_filter, &filter);
    
    // optionally limit the list to a random subset
    if ( cnt < objs.size() )
    {
        objs.shuffle();
        objs.truncate(cnt);
    }
    
    simul.mark(objs, mrk);
}


void Interface::execute_cut(std::string const& name, Glossary& opt)
{
    Vector n(1,0,0);
    real a = 0;
    
    opt.set(n, "plane");
    opt.set(a, "plane", 1);
    
    state_t stateP = STATE_RED, stateM = STATE_GREEN;
    opt.set(stateP, "new_end_state");
    opt.set(stateM, "new_end_state", 1);
    
    ObjectList objs;

    if ( name == "all" )
    {
        objs = simul.fibers.collect();
    }
    else
    {
        Property * pp = simul.properties.find_or_die(name);
        if ( pp->category() != "fiber" )
            throw InvalidSyntax("only `cut fiber' is supported");
        
        Filter filter;
        filter.set(simul, pp, opt);
        objs = simul.fibers.collect(pass_filter, &filter);
    }
    
    VLOG("-CUT PLANE (" << n << ").x = " << -a << "\n");
    simul.fibers.planarCut(objs, n, a, stateP, stateM);
}

//------------------------------------------------------------------------------
#pragma mark -

void reportCPUtime(int frame, real simtime)
{
    static int hour = -1;
    int h = TicToc::hours_today();
    if ( hour != h )
    {
        hour = h;
        Cytosim::log << "% " << TicToc::date() << "\n";
    }
    
    static double clk = 0;
    double cpu = double(clock()) / CLOCKS_PER_SEC;
    Cytosim::log("F%-6i  %7.2fs   CPU %10.3fs  %10.0fs\n", frame, simtime, cpu-clk, cpu);
    clk = cpu;
}


/**
 Perform simulation steps. The accepted Syntax is:
 
     run POSITIVE_INTEGER SIMUL_NAME
     {
        duration   = POSITIVE_REAL
        solve      = SOLVE_MODE
        event      = RATE, ( CODE )
        nb_frames  = INTEGER, ( CODE )
        prune      = BOOL
     }
 
 or
 
     run SIMUL_NAME
     {
        nb_steps   = POSITIVE_INTEGER
        ...
     }

 or, without specifying the Name of the Simul:
 
     run [POSITIVE_INTEGER] all simul
     {
        ...
     }

 
 The associated block can specify these parameters:
 
 Parameter    | Default | Description                                          |
 -------------|---------|-------------------------------------------------------
 `nb_steps`   |  1      | number of simulation steps
 `duration`   |  -      | when specified, `nb_steps` is set to `ceil(duration/time_step)`
 `solve`      |  `on`   | Define the type of method used for the mechanics
 `event`      |  `none` | custom code executed stochastically with prescribed rate
 `nb_frames`  |  0      | number of states written to trajectory file
 `prune`      |  `true` | Print only parameters that are different from default
 
 
 The parameter `solve` can be used to select alternative mechanical engines.
 The monte-carlo part of the simulation is always done, including
 fiber assembly dynamics, binding/unbinding and diffusion of molecules.
 
 `solve`      | Result                                                         |
 -------------|-----------------------------------------------------------------
 `off`        | Objects are immobile.
 `on`         | The mechanics is solved fully (default).
 `auto`       | Same as 'on' but preconditionning method is set automatically.
 `horizontal` | The mechanics is solved only allowing motion in the X-direction. 
  
 If set, `event` defines an event occuring at a rate specified by the positive real `RATE`.
 The action is defined by CODE, a string enclosed with parenthesis containing cytosim commands.
 This code will be executed at stochastic times with the specified rate.
 
 Example:

     event = 10, ( new actin { position=(rectangle 1 6); length=0.1; } )
 
 Calling `run` will not output the initial state, but this can be done with a separate command:
 
     export objects objects.cmo { append = 0 }
 
     run 1000 system
     {
        nb_frames = 10
     }
 
 */
void Interface::execute_run(unsigned nb_steps, Glossary& opt, bool do_write)
{
    size_t nb_frames = 0;
    int    solve     = 1;
    bool   prune     = true;
    bool   binary    = true;
    
#ifdef BACKWARD_COMPATIBILITY
    // check if 'event' is specified within the 'run' command,
    // and convert to a registered Event object
    Event * event = nullptr;
    if ( opt.has_key("event") )
    {
        event = new Event();
        opt.set(event->rate, "event");
        opt.set(event->activity, "event", 1);
        event->reload(simul.time());
        simul.events.add(event);
    }
#endif
    opt.set(solve, "solve", {{"off",0}, {"on",1}, {"auto",2}, {"horizontal",3}});
    
    // setting a pointer to the 'solve' function
    void (Simul::* solveFunc)() = &Simul::solve_not;
    switch ( solve )
    {
        case 1: solveFunc = &Simul::solve;      break;
        case 2: solveFunc = &Simul::solve_auto; break;
        case 3: solveFunc = &Simul::solveX;     break;
    }

    opt.set(prune,     "prune");
    opt.set(binary,    "binary");
    opt.set(nb_frames, "nb_frames");
    
    do_write &= ( nb_frames > 0 );

    size_t frame = 0;
    real   delta = real(nb_steps);
    size_t check = nb_steps;
    
    VLOG("+RUN START " << nb_steps << '\n');

    if ( do_write )
    {
        simul.writeProperties(nullptr, prune);
        if ( simul.prop->clear_trajectory )
        {
            simul.writeObjects(TRAJECTORY, false, binary);
            simul.prop->clear_trajectory = false;
        }
        delta = real(nb_steps) / real(nb_frames);
        check = size_t(delta);
    }
    
    simul.prepare();
    
    size_t sss = 0;
    do {
        while ( sss < check )
        {
            hold();
            //fprintf(stderr, "> step %6zu\n", sss);
            (simul.*solveFunc)();
            simul.step();
            ++sss;
        }
        ++frame;
        // next check point:
        check = size_t(delta*(frame+1));

        if ( do_write )
        {
            simul.relax();
            simul.writeObjects(TRAJECTORY, true, binary);
            reportCPUtime(frame, simul.time());
            simul.unrelax();
        }
    } while ( sss < nb_steps );
    
#ifdef BACKWARD_COMPATIBILITY
    if ( event )
        simul.events.erase(event);
#endif
    simul.relax();
    VLOG("+RUN END\n");
}


/**
 Perform plain simulation steps, without any option:
 alternating step() and solve()
*/
void Interface::execute_run(unsigned nb_steps)
{
    VLOG("-RUN START " << nb_steps << '\n');
    simul.prepare();
    
    for ( unsigned sss = 0; sss < nb_steps; ++sss )
    {
        hold();
        //fprintf(stderr, "> step %6i\n", sss);
        simul.solve();
        simul.step();
    }
    
    simul.relax();
    VLOG("-RUN END\n");
}


//------------------------------------------------------------------------------
#pragma mark -

/**
 Import a simulation snapshot from a trajectory file
 
 The frame to be imported can be specified as an option: `frame=INTEGER`:
 
     import objects sim_objects.cmo { frame = 10 }
 
 By default, this will replace the simulation state by the one loaded from file.
 To add the file objects to the simulation without deleting the current world,
 you should specify `append=1`:
 
     import objects sim_objects.cmo { append = 1 }
 
 */
void Interface::execute_import(std::string const& file, std::string const& what, Glossary& opt)
{
    // we could use the 'tag' to select a certain class of object
    ObjectSet * subset = nullptr;
    
    if ( what != "all" && what != "objects" )
    {
        subset = simul.findSet(what);
        if ( !subset )
            throw InvalidIO("expected class specifier (eg. `import all FILE' or `import fiber FILE')");
    }

    Inputter in(DIM, file.c_str(), true);

    if ( ! in.good() )
        throw InvalidIO("Could not open file `"+file+"'");
    
    bool append = false;
    unsigned cnt = 0, frm = 0;

    opt.set(frm, "frame");
    opt.set(append, "append");

    VLOG("-IMPORT frame " << frm << " from " << file << '\n');

    while ( in.good() )
    {
        if ( append )
        {
            real t = simul.prop->time;
            simul.loadObjects(in, subset);
            simul.prop->time = t;
        }
        else
            simul.reloadObjects(in, subset);
        if ( cnt >= frm )
            break;
        ++cnt;
    }
    
    if ( cnt < frm )
        throw InvalidIO("Could not import requested frame");
    
#if ( 0 )
    //unfinished code to mark imported objects
    int mrk;
    if ( opt.set(mrk, "mark") )
    {
         simul.mark(objs, mrk);
    }
#endif
    
    // set time
    real t;
    if ( opt.set(t, "time") )
        simul.prop->time = t;
}


/**
 see Parser::parse_export
 */
void Interface::execute_export(std::string& file, std::string const& what, Glossary& opt)
{
    bool append = true;
    bool binary = true;
    
    opt.set(append, "append");
    opt.set(binary, "binary");

    VLOG("-EXPORT " << what << " to " << file << '\n');
    
    if ( what == "all" || what == "objects" )
    {
        // a '*' designates the current output:
        if ( file == "*" )
            file = simul.prop->trajectory_file;

        simul.writeObjects(file, append, binary);
    }
    else if ( what == "properties" )
    {
        // a '*' designates the usual file name for output:
        if ( file == "*" )
            file = simul.prop->property_file;
        
        simul.writeProperties(file.c_str(), false);
    }
    else
        throw InvalidIO("only `objects' or `properties' can be exported");
}


/**
 see Parser::parse_report
 */
void Interface::execute_report(std::string& file, std::string const& what, Glossary& opt)
{
    bool verbose = true;
    opt.set(verbose, "verbose");
    std::string str;
    VLOG("-WRITE " << what << " to " << file << '\n');
    
    std::ostream * osp = &std::cout;
    std::ofstream ofs;

    // a STAR designates the standard output:
    if ( file != "*" )
    {
        bool append = true;
        opt.set(append, "append");
        ofs.open(file.c_str(), append ? std::ios_base::app : std::ios_base::out);
        osp = &ofs;
    }
    
    if ( verbose )
    {
        simul.report(*osp, what, opt);
    }
    else
    {
        std::stringstream ss;
        simul.report(ss, what, opt);
        StreamFunc::skip_lines(*osp, ss, '%');
    }
    
    if ( ofs.is_open() )
        ofs.close();
}


void Interface::execute_call(std::string& str, Glossary& opt)
{
    if ( str == "equilibrate" )
        simul.couples.equilibrate(simul.fibers, simul.properties);
    else if ( str == "connect" )
        simul.couples.bindToIntersections(simul.fibers, simul.properties);
    else if ( str == "custom0" )
        simul.custom0(opt);
    else if ( str == "custom1" )
        simul.custom1(opt);
    else if ( str == "custom2" )
        simul.custom2(opt);
    else if ( str == "custom3" )
        simul.custom3(opt);
    else if ( str == "custom4" )
        simul.custom4(opt);
    else if ( str == "custom5" )
        simul.custom5(opt);
    else if ( str == "custom6" )
        simul.custom6(opt);
    else if ( str == "custom7" )
        simul.custom7(opt);
    else if ( str == "custom8" )
        simul.custom8(opt);
    else if ( str == "custom9" )
        simul.custom9(opt);
    else
        throw InvalidSyntax("called unknown command");
}

