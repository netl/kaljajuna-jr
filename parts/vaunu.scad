module can(){
    tolerance = 1;
    h = 95;
    diameter = 66;
    end_diameter = 53;
    chamfer = 16.5;
    translate([0,0,(-h-tolerance)/2]){
        union(){

        //frame
        cylinder(d=66+tolerance,h=h+tolerance);

        //top
        translate([0,0,h+tolerance])
            cylinder(d1=diameter+tolerance, d2=end_diameter+tolerance, h=chamfer);

        //bottom 
        rotate([180,0,0])
            cylinder(d1=diameter+tolerance, d2=end_diameter+tolerance, h=chamfer);
        }
    }
}

l = 140;
w = 58;

//main holder
translate([-l/2,-w/2,0])
    difference(){
        //carriage
        cube([l,58,15]);

        //can
        translate([l/2,58/2,35])
            rotate([0,90,0])
                can();
    }
