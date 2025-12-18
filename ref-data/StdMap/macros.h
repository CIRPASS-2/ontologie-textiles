#define _IF_BOUND(x,y)  bind(if(bound(?y),#x,?UNDEF) as ?x##_IF_BOUND)
#define LV95(x)         bind(concat("<https://www.opengis.net/def/crs/EPSG/0/2056>",x) as x##_LV95)
#define SPLIT(x,y,z)    z apf:strSplit (x y).
#define SPLIT_SEMI(x)   SPLIT(x,"; ?",x##_SPLIT_SEMI)
#define NO_SPACE(x)     bind(replace(x," ","") as x##_NO_SPACE)
