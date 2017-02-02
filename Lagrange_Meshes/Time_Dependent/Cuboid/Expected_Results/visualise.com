gfx read nodes /people/kcla882/b.exregion
gfx define field Coordinate coordinate_system rectangular_cartesian finite_element number_of_components 3 coordinate real component_names x y z;
# field DiffusionRegion created by other commands
# field DiffusionRegion.nodes created by other commands
gfx define field U coordinate_system rectangular_cartesian finite_element number_of_components 1 field real component_names 1;
gfx define field cmiss_number coordinate_system rectangular_cartesian cmiss_number;
gfx define field "del U_del n" coordinate_system rectangular_cartesian finite_element number_of_components 1 field real component_names 1;
gfx modify spectrum default clear overwrite_colour;
gfx modify spectrum default linear reverse range 0 1 extend_above extend_below rainbow colour_range 0 1 component 1;
gfx create material black normal_mode ambient 0 0 0 diffuse 0 0 0 emission 0 0 0 specular 0.3 0.3 0.3 alpha 1 shininess 0.2;
gfx create material blue normal_mode ambient 0 0 1 diffuse 0 0 1 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material bone normal_mode ambient 0.7 0.7 0.6 diffuse 0.9 0.9 0.7 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material brown normal_mode ambient 0.5 0.25 0 diffuse 0.5 0.25 0 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material cyan normal_mode ambient 0 1 1 diffuse 0 1 1 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material default normal_mode ambient 1 1 1 diffuse 1 1 1 emission 0 0 0 specular 0 0 0 alpha 1 shininess 0;
gfx create material default_selected normal_mode ambient 1 0.2 0 diffuse 1 0.2 0 emission 0 0 0 specular 0 0 0 alpha 1 shininess 0;
gfx create material gold normal_mode ambient 1 0.4 0 diffuse 1 0.7 0 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.3;
gfx create material gray50 normal_mode ambient 0.5 0.5 0.5 diffuse 0.5 0.5 0.5 emission 0.5 0.5 0.5 specular 0.5 0.5 0.5 alpha 1 shininess 0.2;
gfx create material green normal_mode ambient 0 1 0 diffuse 0 1 0 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material grey25 normal_mode ambient 0.25 0.25 0.25 diffuse 0.25 0.25 0.25 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material grey50 normal_mode ambient 0.5 0.5 0.5 diffuse 0.5 0.5 0.5 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material grey75 normal_mode ambient 0.75 0.75 0.75 diffuse 0.75 0.75 0.75 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material magenta normal_mode ambient 1 0 1 diffuse 1 0 1 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material muscle normal_mode ambient 0.4 0.14 0.11 diffuse 0.5 0.12 0.1 emission 0 0 0 specular 0.3 0.5 0.5 alpha 1 shininess 0.2;
gfx create material orange normal_mode ambient 1 0.5 0 diffuse 1 0.5 0 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material red normal_mode ambient 1 0 0 diffuse 1 0 0 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material silver normal_mode ambient 0.4 0.4 0.4 diffuse 0.7 0.7 0.7 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.3;
gfx create material tissue normal_mode ambient 0.9 0.7 0.5 diffuse 0.9 0.7 0.5 emission 0 0 0 specular 0.2 0.2 0.3 alpha 1 shininess 0.2;
gfx create material transparent_gray50 normal_mode ambient 0.5 0.5 0.5 diffuse 0.5 0.5 0.5 emission 0.5 0.5 0.5 specular 0.5 0.5 0.5 alpha 0 shininess 0.2;
gfx create material white normal_mode ambient 1 1 1 diffuse 1 1 1 emission 0 0 0 specular 0 0 0 alpha 1 shininess 0;
gfx create material yellow normal_mode ambient 1 1 0 diffuse 1 1 0 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
