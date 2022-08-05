import torch

change_dict_11 = {
    # conv1  - 1 block
    "features.0.":  "conv1.",
    # layer1 - 1 block
    "features.1.":  "layer1.0.",
    # layer2 - 2 block
    "features.2.":  "layer2.0.",
    "features.3.":  "layer2.1.",
    # layer3 - 3 block
    "features.4.":  "layer3.0.",
    "features.5.":  "layer3.1.",
    "features.6.":  "layer3.2.",
    # layer4 - 4 block
    "features.7.":  "layer4.0.",
    "features.8.":  "layer4.1.",
    "features.9.":  "layer4.2.",
}
change_dict_12 = {
    # layer4 - 4 block
    "features.10.": "layer4.3.",
    # layer5 - 3 block
    "features.11.": "layer5.0.",
    "features.12.": "layer5.1.",
    "features.13.": "layer5.2.",
    # layer6 - 3 block
    "features.14.": "layer6.0.",
    "features.15.": "layer6.1.",
    "features.16.": "layer6.2.",
    # layer7 - 1 block
    "features.17.": "layer7.0.",
    # conv2  - 1 block
    "features.18.": "conv2.",
}

ckpt_path = "/workdir/checkpoint/mobilenetv2/mv2/checkpoint-best.pth"
ckpt = torch.load(ckpt_path)
ckpt_2 = ckpt 
ckpt_2_path = "/workdir/checkpoint/mobilenetv2/mv2/checkpoint-best_mmdet.pth"

state_dict = ckpt["model"]
state_dict_2 = {}

for name in state_dict:
    parameters = state_dict[name]
    print(name, parameters.shape)
    if name[:11] in change_dict_11:
        new_name = change_dict_11[name[:11]]+name[11:]
    elif name[:12] in change_dict_12:
        new_name = change_dict_12[name[:12]]+name[12:]
    else:
        continue
    state_dict_2[new_name] = parameters
    print(new_name, parameters.shape)

print(state_dict.keys())
print(state_dict_2.keys())

ckpt_2["model"] = state_dict_2
torch.save(ckpt_2, ckpt_2_path)
