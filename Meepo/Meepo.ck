// Meepo.ck
// Eric Heep, May 2016
// communication

public class Meepo {
    // serial setup
    SerialIO serial;
    SerialIO.list() @=> string list[];
    
    // initialize
    fun void init() {
        int serial_port;
        
        for (int i; i < list.cap(); i++) {
            if (list[i].find("usb") > 0) {
                i => serial_port;
                <<< "Connected to", list[i] >>>;
            }
        }
        
        // serial connecting
        if (!serial.open(serial_port, SerialIO.B57600, SerialIO.BINARY)) {
            <<< "Unable to open serial device:", "\t", list[serial_port] >>>;
        }
        else {
            <<< list[serial_port], "assigned to port", serial_port, "" >>>;
        }
        
        2.0::second => now;
    }
    
    // note function
    fun void note(int num, int vel) {
        // allows note numbers 0-63 and note velocities 0-1023
        int bytes[3];
        255 => bytes[0];
        (num << 2) | (vel >> 8) => bytes[1];
        vel & 255 => bytes[2];
        serial.writeBytes(bytes);
    }
}


Meepo meep;
meep.init();

fun void Solenoids(){
    while (true) {
        meep.note(0, 127);
        Math.random2f(0.1, 0.5)::second => now;
        meep.note(1, 127);
        Math.random2f(0.1, 0.5)::second => now;
    }
}


fun void Motors(){
    while(true){
        meep.note(2, 127);
        Math.random2f(500, 2000)::ms => now;
        meep.note(3, 127);
        Math.random2f(500, 2000)::ms => now;
        meep.note(4, 127);
        Math.random2f(100, 1000)::ms => now;
    }
}

spork ~ Solenoids();
spork ~ Motors();

while(1){
    Solenoids();
    50::ms => now;
}





