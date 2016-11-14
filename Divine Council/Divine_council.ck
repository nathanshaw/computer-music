// Divine Council Composition
OscOut out;

// ("chuckServer.local", 50000) => out.dest;
("localhost", 50000) => out.dest;

fun void gods1(int note, int vel, int delay){
    out.start("/brigid4");
    out.add(note);
    out.add(vel);
    out.send();
    out.start("/brigid1");
    out.add(note);
    out.add(vel);
    out.send();
    delay::ms => now;
    out.start("/brigid4");
    out.add(note);
    out.add(0);
    out.send();
    out.start("/brigid1");
    out.add(note);
    out.add(0);
    out.send();
}

fun void gods2(int note, int vel, int delay){
    out.start("/brigid5");
    out.add(note);
    out.add(vel);
    out.send();
    out.start("/brigid2");
    out.add(note);
    out.add(vel);
    out.send();
    delay::ms => now;
    out.start("/brigid5");
    out.add(note);
    out.add(0);
    out.send();
    out.start("/brigid2");
    out.add(note);
    out.add(0);
    out.send();
}

fun void gods3(int note, int vel, int delay){
    out.start("/brigid6");
    out.add(note);
    out.add(vel);
    out.send();
    out.start("/brigid3");
    out.add(note);
    out.add(vel);
    out.send();
        delay::ms => now;
    out.start("/brigid6");
    out.add(note);
    out.add(0);
    out.send();
    out.start("/brigid3");
    out.add(note);
    out.add(0);
    out.send();
}

fun void stairwayToHeavan(int note, int vel){
    out.start("/hermes1");
    out.add(note);
    out.add(vel);
    out.send();
}



while(true) {
    for (int i; i < 6; i++) {
        i + 60 => int note;
        spork ~ stairwayToHeavan(Math.random2(60,64), 
                                 Math.random2(100,1023));
        spork ~ gods3(note, 500, 10);
        Math.random2(5, 50)::ms => now;
    }
    //200::ms => now;
}
