#!/bin/bash
#SBATCH --job-name=chen   
#SBATCH --output=output_log.txt      
#SBATCH --error=error_log.txt   
#SBATCH --gres=gpu:v100:1 
#SBATCH --mem=16G                   
#SBATCH --time=06:00:00                
#SBATCH --account=csci5525    
#SBATCH --mail-user=chen8596@umn.edu           
              

echo "Starting job on $(hostname) at $(date)"

cd ~/MediConfusion

python scripts/answering.py --mllm_name gpt --mode mc

echo "Job finished with exit code $? at: $(date)"
