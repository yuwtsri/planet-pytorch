import torch.nn as nn
import torch.nn.functional as F
import utils



class PlanetSimpleNet(nn.Module):

    """Simple 3 layer convnet. Assumes 64x64 input"""


    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 8 * 8, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 17),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 256 * 8 * 8)
        x = self.classifier(x)
        return F.sigmoid(x)

if __name__ == '__main__':
    net = PlanetSimpleNet()
    size = utils.calculate_feature_size(net.features, (64, 64))
    print(size)
