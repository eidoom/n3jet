#include <cmath>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "model_fns.h"

using namespace std;

int main()
{
  cout.setf(ios_base::scientific, ios_base::floatfield);
  cout.precision(16);

  cout << endl;
  cout << "n3jet: simple example of calling a pretrained neural network for inference in a C++ interface" << endl;
  cout << endl;

  const int legs = 5;
  const int pspoints = 2;
  const int training_reruns = 20;

  //raw momenta input

  double Momenta[pspoints][legs][4] = {
				     {
				       {500.,   0.,   0., 500.},
				       {500.,   0.,   0., -500.},
				       {253.58419798, -239.58965912, 66.81985738, -49.36443422},
				       {373.92489886,    7.43568582, -321.18384469,  191.32558238},
				       {372.49090317,  232.1539733 ,  254.36398731, -141.96114816}
				     },
				     {
				       {500.,   0.,   0., 500.},
				       {500.,   0.,   0., -500.},
				       {253.58419798, -239.58965912, 66.81985738, -49.36443422},
				       {373.92489886,    7.43568582, -321.18384469,  191.32558238},
				       {372.49090317,  232.1539733 ,  254.36398731, -141.96114816}
				     }
  };
  
  string model_base = "./models/diphoton/3g2A/RAMBO/";
  string model_dirs[training_reruns] = {"events_100k_single_all_legs_all_save_0/",
			"events_100k_single_all_legs_all_save_1/",
			"events_100k_single_all_legs_all_save_2/",
			"events_100k_single_all_legs_all_save_3/",
			"events_100k_single_all_legs_all_save_4/",
			"events_100k_single_all_legs_all_save_5/",
			"events_100k_single_all_legs_all_save_6/",
			"events_100k_single_all_legs_all_save_7/",
			"events_100k_single_all_legs_all_save_8/",
			"events_100k_single_all_legs_all_save_9/",
			"events_100k_single_all_legs_all_save_10/",
			"events_100k_single_all_legs_all_save_11/",
			"events_100k_single_all_legs_all_save_12/",
			"events_100k_single_all_legs_all_save_13/",
			"events_100k_single_all_legs_all_save_14/",
			"events_100k_single_all_legs_all_save_15/",
			"events_100k_single_all_legs_all_save_16/",
			"events_100k_single_all_legs_all_save_17/",
			"events_100k_single_all_legs_all_save_18/",
			"events_100k_single_all_legs_all_save_19/"
  };

  vector<vector<double> > metadatas(training_reruns, vector<double>(10));

  for (int i = 0; i < training_reruns; i++){
    string metadata_file = model_base + model_dirs[i] + "dataset_metadata.dat";
    vector<double> metadata = read_metadata_from_file(metadata_file);
    for (int j = 0; j < 10 ; j++){
      metadatas[i][j] = metadata[j];
    };
  };

  string model_dir_models[training_reruns];
  for (int k = 0; k < training_reruns; k++){
    model_dir_models[k] = model_base + model_dirs[k] + "model.dat";
  };
  
  KerasModel kerasModel_0(model_dir_models[0]);
  KerasModel kerasModel_1(model_dir_models[1]);
  KerasModel kerasModel_2(model_dir_models[2]);
  KerasModel kerasModel_3(model_dir_models[3]);
  KerasModel kerasModel_4(model_dir_models[4]);
  KerasModel kerasModel_5(model_dir_models[5]);
  KerasModel kerasModel_6(model_dir_models[6]);
  KerasModel kerasModel_7(model_dir_models[7]);
  KerasModel kerasModel_8(model_dir_models[8]);
  KerasModel kerasModel_9(model_dir_models[9]);
  KerasModel kerasModel_10(model_dir_models[10]);
  KerasModel kerasModel_11(model_dir_models[11]);
  KerasModel kerasModel_12(model_dir_models[12]);
  KerasModel kerasModel_13(model_dir_models[13]);
  KerasModel kerasModel_14(model_dir_models[14]);
  KerasModel kerasModel_15(model_dir_models[15]);
  KerasModel kerasModel_16(model_dir_models[16]);
  KerasModel kerasModel_17(model_dir_models[17]);
  KerasModel kerasModel_18(model_dir_models[18]);
  KerasModel kerasModel_19(model_dir_models[19]);
  

}
