#include <webots/robot.h>
#include <webots/supervisor.h>
#include <webots/touch_sensor.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define TIME_STEP 32

//Change the defines accordingly
#define HIT_DELAY 1
#define STUCK_TIME 120
#define HIT_DIS 0.1
//Change the corresponding DEF robot name of the competitors
#define ROBOT_NAME "rebel" 

int main(int argc, char **argv) {
  
  //vriables
  WbDeviceTag wall;
  int hits = 0;
  
  double t = wb_robot_get_time();
  double initial_pos[3] = {-1.74,1.13,0};
  double pre_hit_pos[3] = {initial_pos[0],initial_pos[1],initial_pos[2]};
  double box1_initial_pos[3] = {initial_pos[0]+2.22,initial_pos[1],0.015};
  double box2_initial_pos[3] = {initial_pos[0]+2.22,initial_pos[1]-2.22,0.02};
  double box3_initial_pos[3] = {initial_pos[0],initial_pos[1]-2.22,0.025};
  double dist;
  bool hit = false;
  
  //Intialize supervisor robot
  wb_robot_init();
  
  //Check for the competitor robot is available
  WbNodeRef robot_node = wb_supervisor_node_get_from_def(ROBOT_NAME);
  if (robot_node == NULL) {
    fprintf(stderr, "No DEF robot node found in the current world file\n");
    exit(1);
  }
  
  //Access the translation of the robot and move to start position
  WbFieldRef robot_trans = wb_supervisor_node_get_field(robot_node, "translation");
  wb_supervisor_field_set_sf_vec3f(robot_trans, initial_pos);
  wb_supervisor_node_reset_physics(robot_node);
  
  //settng Boxes positions
  WbNodeRef box1 = wb_supervisor_node_get_from_def("box_1");
  WbFieldRef box1_trans = wb_supervisor_node_get_field(box1, "translation");
  wb_supervisor_field_set_sf_vec3f(box1_trans, box1_initial_pos);
  wb_supervisor_node_reset_physics(box1);
  
  WbNodeRef box2 = wb_supervisor_node_get_from_def("box_2");
  WbFieldRef box2_trans = wb_supervisor_node_get_field(box2, "translation");
  wb_supervisor_field_set_sf_vec3f(box2_trans, box2_initial_pos);
  wb_supervisor_node_reset_physics(box2);
  
  WbNodeRef box3 = wb_supervisor_node_get_from_def("box_3");
  WbFieldRef box3_trans = wb_supervisor_node_get_field(box3, "translation");
  wb_supervisor_field_set_sf_vec3f(box3_trans, box3_initial_pos);
  wb_supervisor_node_reset_physics(box3);
  
  //Access wall sensor
  wall = wb_robot_get_device("wall_sensor");
  wb_touch_sensor_enable(wall, TIME_STEP);
  
  
  
  while (wb_robot_step(TIME_STEP) != -1) {
    
    if (wb_touch_sensor_get_value(wall)){
      
      const double *hit_pos = wb_supervisor_field_get_sf_vec3f(robot_trans);
      dist = sqrt((hit_pos[0]-pre_hit_pos[0]) * (hit_pos[0]-pre_hit_pos[0]) + (hit_pos[1]-pre_hit_pos[1]) * (hit_pos[1]-pre_hit_pos[1]));
            
      if(dist>HIT_DIS && hit==false){
        hits+=1;
        
        t = wb_robot_get_time();
        pre_hit_pos[0] = hit_pos[0];
        pre_hit_pos[1] = hit_pos[1];
        pre_hit_pos[2] = hit_pos[2];
        printf("Hit!! : total hits = %d\n",hits);
      }
      else{
      
        if((wb_robot_get_time()-t)>=STUCK_TIME){
          break;
        }
      }
      hit = true;
    }
    else{
        hit = false;
    }

  }
  fprintf(stderr, " >>> Robot stuck for %d seconds !!!\n",STUCK_TIME);
  fprintf(stderr, " >>> Restart the simulation (Maybe try different initial conditions)\n");
  fprintf(stderr, " >>> Supervisor robot exiting ... \n");  

  wb_robot_cleanup();

  return 0;
}
