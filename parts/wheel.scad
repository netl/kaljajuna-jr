$fn = 30;

wheel_diameter = 17;
wheel_width = 4.5;
lip_diameter = 23.8;
lip_width = 2;
support_width = 2;
shaft_diameter = 4.3;

difference(){
    union(){
        //wheel
        translate([0,0,lip_width+support_width])
            cylinder(h=wheel_width, d=wheel_diameter);

        //lip
        translate([0,0,support_width])
            cylinder(d1=lip_diameter, d2=17, h=lip_width);

        //support
        cylinder(d=lip_diameter, h=support_width);
    }

    //shaft
    cylinder(d=shaft_diameter, h=support_width+lip_width+wheel_width);
}
