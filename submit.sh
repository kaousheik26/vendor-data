#!/bin/bash
#SBATCH --nodes=1
#SBATCH --partition=testp
#SBATCH --cpus-per-task=32
#SBATCH --gres=gpu:A100-SXM4:2
#SBATCH --time=2-23:00:00
#SBATCH --error=job.%J.err
#SBATCH --output=slurm.%J.out
#cd $SLURM_SUBMIT_DIR
#cd /nlsasfs/home/sysadmin/nazgul/gpu-burn-master
echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
echo "Job id is $SLURM_JOBID"
echo "Job submission directory is : $SLURM_SUBMIT_DIR"
#srun ./gpu_burn -tc -d 3600 #
#srun /bin/hostname

tgt=be_en
fairseq-train     /nlsasfs/home/nltm-pilot/jkaoushe/mt/$tgt/data-bin/iwslt14.tokenized.$tgt     --arch transformer_iwslt_de_en --share-decoder-input-output-embed     --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0     --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000     --dropout 0.3 --weight-decay 0.0001     --criterion label_smoothed_cross_entropy --label-smoothing 0.1     --max-tokens 4096     --eval-bleu     --eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}'     --eval-bleu-detok moses     --eval-bleu-remove-bpe     --eval-bleu-print-samples     --best-checkpoint-metric bleu --maximize-best-checkpoint-metric --save-dir /nlsasfs/home/nltm-pilot/jkaoushe/mt/$tgt/data-bin/checkpoints --max-epoch 80
