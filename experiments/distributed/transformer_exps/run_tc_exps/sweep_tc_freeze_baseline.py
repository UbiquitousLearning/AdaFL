import argparse
import logging
import os
from time import sleep


def add_args(parser):
    """
    parser : argparse.ArgumentParser
    return a parser added with args required by fit
    """
    return parser.parse_args()


def wait_for_the_training_process(args):
    pipe_path = "./tmp/fedml-baseline-{args.dataset}".format(args=args)
    pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
    with os.fdopen(pipe_fd) as pipe:
        while True:
            message = pipe.read()
            if message:
                print("Received: '%s'" % message)
                print("Training is finished. Start the next training with...")
                os.remove(pipe_path)
                return
            sleep(3)
            # print("Daemon is alive. Waiting for the training result.")

def set_hp(delta_round, freeze_layers, args):
        if args.dataset == "agnews":
            partition_method = "niid_label_clients=1000_alpha=10.0"
        if args.dataset == "semeval_2010_task8":
            partition_method = "niid_label_clients=100_alpha=100"
        if args.dataset == "20news":
            partition_method = "uniform"

        hp = 'FedAvg ' + partition_method + ' 0.1 0.1 ' + str(delta_round) + ' 5 ' + remove_space(str([freeze_layers[2]]).replace(',','.')+','+str([-1]).replace(',','.')+','+str(freeze_layers[2]))+','+str(freeze_layers[3][-1]).replace(',','.')+" "+str(args.depth)+" "+str(args.time_threshold) +" "+str(args.dataset) + " shallow" # linux 读取输入的时候以，为分隔符，需要替换掉

        return hp

def remove_space(s):
    s_no_space = ''.join(s.split())
    return s_no_space

def remove_cache_model(args):
    os.system("rm -rf .\/tmp\/{args.dataset}_fedavg_output_baseline-{args.depth}-{args.time_threshold}".format(args=args))

# customize the log format
logging.basicConfig(level=logging.INFO,
                    format='%(process)s %(asctime)s.%(msecs)03d - {%(module)s.py (%(lineno)d)} - %(funcName)s(): %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S')

parser = argparse.ArgumentParser()
args = add_args(parser)

# os.system("kill $(ps aux | grep \"fedavg_main_tc.py\" | grep -v grep | awk '{print $2}')")

# sh run_text_classification.sh FedAvg "niid_label_clients=100_alpha=5.0" 5e-5 0.1 30
# sh run_text_classification.sh FedAvg "niid_label_clients=100_alpha=10.0" 5e-5 0.1 30
# sh run_text_classification.sh FedAvg "niid_label_clients=100_alpha=1.0" 5e-5 0.1 30
# sh run_text_classification.sh FedAvg "uniform" 5e-5 0.1 30
# sh run_text_classification.sh FedAvg "niid_quantity_clients=100_beta=5.0" 5e-5 0.1 30

# sh run_text_classification.sh FedProx "niid_label_clients=100_alpha=5.0" 5e-5 0.1 30
# sh run_text_classification.sh FedProx "niid_label_clients=100_alpha=10.0" 5e-5 0.1 30
# sh run_text_classification.sh FedProx "niid_label_clients=100_alpha=1.0" 5e-5 0.1 30
# sh run_text_classification.sh FedProx "uniform" 5e-5 0.1 30
# sh run_text_classification.sh FedProx "niid_quantity_clients=100_beta=5.0" 5e-5 0.1 30

# sh run_text_classification.sh FedOPT "niid_label_clients=100_alpha=5.0" 5e-5 0.1 30
# sh run_text_classification.sh FedOPT "niid_label_clients=100_alpha=10.0" 5e-5 0.1 30
# sh run_text_classification.sh FedOPT "niid_label_clients=100_alpha=1.0" 5e-5 0.1 30
# sh run_text_classification.sh FedOPT "uniform" 5e-5 0.1 30
# sh run_text_classification.sh FedOPT "niid_quantity_clients=100_beta=5.0" 5e-5 0.1 30

hps = [
    # 'FedAvg "niid_label_clients=100_alpha=5.0" 5e-5 0.1 25', # finished by Zihang
    # 'FedAvg "niid_label_clients=100_alpha=10.0" 5e-5 0.1 25',
    # 'FedAvg "niid_label_clients=100_alpha=1.0" 5e-5 0.1 25',
    # 'FedProx "niid_label_clients=100_alpha=5.0" 5e-5 0.1 25',
    # 'FedProx "niid_label_clients=100_alpha=10.0" 5e-5 0.1 25',
    # 'FedProx "niid_label_clients=100_alpha=1.0" 5e-5 0.1 25',
    # 'FedOPT "niid_label_clients=100_alpha=5.0" 5e-5 0.1 25',
    # 'FedOPT "niid_label_clients=100_alpha=10.0" 5e-5 0.1 25',
    # 'FedOPT "niid_label_clients=100_alpha=1.0" 5e-5 0.1 25',
    # 'FedAvg "uniform" 5e-5 0.1 25',
    # 'FedProx "uniform" 5e-5 0.1 25',
    # 'FedOPT "uniform" 5e-5 0.1 25',
    # 'FedAvg "niid_quantity_clients=100_beta=5.0" 5e-5 0.1 25',
    # 'FedOPT "niid_quantity_clients=100_beta=5.0" 5e-5 0.1 25', # finished by Chaoyang
    # 'FedAvg "uniform" 0.1 1 400 10 e,0,1,2,3,4,5',
    # 'FedAvg "uniform" 0.1 1 400 10 e,0,1,2,3,4,5,6,7,8,9,10,11',
    # 'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3,4,5,6,7,8,9,10',
    # 'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3,4,5,6,7,8,9',
    'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3,4,5,6,7,8',
    # 'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3,4,5,6,7',
    'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3,4,5,6',
    # 'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3,4,5',
    'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3,4',
    # 'FedAvg "uniform" 0.1 1 400 5 e,0,1,2,3',
    'FedAvg "uniform" 0.1 1 400 5 e,0,1,2',
    # 'FedAvg "uniform" 0.1 1 400 5 e,0,1',
    'FedAvg "uniform" 0.1 1 400 5 e,0',
    'FedAvg "uniform" 0.1 1 400 5 e'
]

hps_parallelism = [
    'FedAvg "uniform" 0.1 1 200 1',
    'FedAvg "uniform" 0.1 1 200 2',
    'FedAvg "uniform" 0.1 1 200 4',
    'FedAvg "uniform" 0.1 1 200 8',
    'FedAvg "uniform" 0.1 1 200 16',
    'FedAvg "uniform" 0.1 1 200 32',
    # 'FedAvg "uniform" 0.1 1 3000 64',
]

args.round = -1 
args.depth = 0
args.width = 8
args.time_threshold = 60
args.max_round = 3000
args.dataset = "agnews" # "agnews", "20news", "semeval_2010_task8"

# freeze_layers = [[depth],[round],depth,[width]] 
width = [32, 40, 48, 56, 64]
depth = [0,1,2,3,4,5,6]
freeze_layers = [[6],[-1],6,[width]] 

remove_cache_model(args)

run_id = 0

for w in width:
    for d in depth:
        args.depth = d
        args.width = w
        freeze_layers = [[d],[-1],d,[w]] 
        args.hp = set_hp(3000, freeze_layers,args)
        args.run_id = run_id
        
        logging.info("hp = %s" % args.hp)
        # os.system("perl -p -i -e 's/pipe_path = .*/pipe_path = \".\/tmp\/fedml-baseline-{args.dataset}\"/g' /home/cdq/FedNLP/FedML/fedml_api/distributed/fedavg/utils.py".format(args=args)) # pipe tmp name
        # logging.info("perl -p -i -e 's/pipe_path = .*/pipe_path = \".\/tmp\/fedml-baseline-{args.dataset}\"/g' /home/cdq/FedNLP/FedML/fedml_api/distributed/fedavg/utils.py".format(args=args))

        
        os.system("mkdir ./tmp/; touch ./tmp/fedml-baseline-{args.dataset}; mkdir ./results/BERT/{args.dataset}-baseline".format(args=args))
        logging.info('nohup sh run_text_classification_freeze_baseline.sh '
                '{args.hp} '
                '> ./results/BERT/{args.dataset}-baseline/fednlp_tc_width_{args.width}_depth_{args.depth}.log 2>&1 &'.format(args=args))
        os.system('nohup sh run_text_classification_freeze_baseline.sh '
                '{args.hp} '
                '> ./results/BERT/{args.dataset}-baseline/fednlp_tc_width_{args.width}_depth_{args.depth}.log 2>&1 &'.format(args=args))
        

        wait_for_the_training_process(args)

        sleep(5)
        run_id += 1
