python general_init_model_rerun.py \
--mom_file /mt/batch/jbullock/Sherpa_NJet/runs/diphoton/3g2A/RAMBO/momenta_events_100k.npy \
--nj_file /mt/batch/jbullock/Sherpa_NJet/runs/diphoton/3g2A/RAMBO/events_100k_loop.npy \
--delta_near 0.02 \
--model_base_dir /scratch/jbullock/Sherpa_NJet/runs/diphoton/3g2A/RAMBO/ \
--model_dir events_100k_fks_all_legs_all_pairs_all_save \
--training_reruns 20 \
--all_legs True \
--all_pairs True