// Divine Council Composition
OscOut out;

// ("chuckServer.local", 50000) => out.dest;
("localhost", 50000) => out.dest;

fun void gods1(int note, int vel){
    out.start("/brigid4");
    out.add(note);
    out.add(vel);
    out.send();
    out.start("/brigid1");
    out.add(note);
    out.add(vel);
    out.send();
}

fun void gods2(int note, int vel){
    out.start("/brigid5");
    out.add(note);
    out.add(vel);
    out.send();
    out.start("/brigid2");
    out.add(note);
    out.add(vel);
    out.send();
}

fun void gods3(int note, int vel){
    out.start("/brigid6");
    out.add(note);
    out.add(vel);
    out.send();
    out.start("/brigid3");
    out.add(note);
    out.add(vel);
    out.send();
}

fun void stairwayToHeavan(int note, int vel){
    out.start("/hermes1");
    out.add(note);
    out.add(vel);
    out.send();
}

fun void stPlay(int note, int vel, int msDelay){
    spork ~ stSend(note, vel);
    msDelay::ms => now;
    spork ~ stSend(note, 0);
}

while(true) {

}

