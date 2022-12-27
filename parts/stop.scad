difference(){
    cube([100,8,8]);
    rotate([0,-22.5,0])
        cube([25,8,8]);
    translate([100,8,0])
        rotate([0,-22.5,180])
            cube([25,8,8]);
}
