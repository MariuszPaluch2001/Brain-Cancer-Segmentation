from torch import nn

from torch import cat, nn
from torchvision.transforms.functional import center_crop


class SingleConv2D(nn.Module):
    def __init__(self, in_channels, num_filters_conv):
        super().__init__()
        self.seq_single_conv = nn.Sequential(
            nn.Conv2d(
                in_channels=in_channels,
                out_channels=num_filters_conv,
                kernel_size=3,
                padding=1,
            ),
            nn.BatchNorm2d(num_filters_conv),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.seq_single_conv(x)


class DoubleConv(nn.Module):
    def __init__(self, in_channels, num_filters_conv1, num_filters_conv2):
        super().__init__()
        self.double_conv = nn.Sequential(
            SingleConv2D(in_channels, num_filters_conv1),
            SingleConv2D(num_filters_conv1, num_filters_conv2),
        )

    def forward(self, x):
        return self.double_conv(x)


class Up(nn.Module):
    def __init__(self, in_channels, mode="conv_transp"):
        super().__init__()

        if mode == "conv_transp":
            self.upsampling = nn.ConvTranspose2d(
                in_channels=in_channels,
                out_channels=in_channels // 2,
                kernel_size=2,
                stride=2,
            )
        elif mode == "bilinear":
            self.upsampling = nn.sequential(
                nn.Upsample(scale_factor=2, mode="bilinear", align_corners=True),
                SingleConv2D(in_channels, in_channels // 2),
            )
        else:
            raise ValueError("Upsampling method not recognized")

    def forward(self, x):
        return self.upsampling(x)


def concatenate_tensors(x1, x2):
    x2 = center_crop(x2, [x1.shape[2], x1.shape[3]])

    return cat((x1, x2), dim=1)


class Encoder(nn.Module):
    def __init__(self, in_channels, num_filters_conv1, num_filters_conv2):
        super().__init__()
        if num_filters_conv2 % 2 != 0:
            raise ValueError(
                "Encoder can not have odd number of filters (channels) in the second convolutional layer."
            )

        self.encoder = DoubleConv(in_channels, num_filters_conv1, num_filters_conv2)
        self.pool = nn.MaxPool2d(kernel_size=(2, 2))

    def forward(self, x):
        x = self.encoder(x)
        x_down = self.pool(x)
        return x, x_down


class Decoder(nn.Module):
    def __init__(
        self,
        in_channels,
        num_filters_conv1,
        num_filters_conv2,
        upsampling_mode="conv_transp",
    ):
        super().__init__()
        self.doubleConv = DoubleConv(in_channels, num_filters_conv1, num_filters_conv2)
        self.upsampling = Up(in_channels, mode=upsampling_mode)

    def forward(self, x_decoder, x):
        x = self.upsampling(x)
        x = concatenate_tensors(x_decoder, x)

        return self.doubleConv(x)


class UNet2D(nn.Module):
    def __init__(self, input_n_channels, target_n_labels, mode_up="conv_transp"):
        super().__init__()
        self.input_n_channels = input_n_channels
        self.target_n_labels = target_n_labels

        self.encoder1 = Encoder(self.input_n_channels, 64, 64)
        self.encoder2 = Encoder(64, 128, 128)
        self.encoder3 = Encoder(128, 256, 256)
        self.encoder4 = Encoder(256, 512, 512)

        self.encoder_bottom = Encoder(512, 1024, 1024)

        self.decoder4 = Decoder(512 + 512, 512, 512, upsampling_mode=mode_up)
        self.decoder3 = Decoder(256 + 256, 256, 256, upsampling_mode=mode_up)
        self.decoder2 = Decoder(128 + 128, 128, 128, upsampling_mode=mode_up)
        self.decoder1 = Decoder(64 + 64, 64, 64, upsampling_mode=mode_up)

        self.outConv = nn.Conv2d(64, self.target_n_labels, kernel_size=(1, 1))

    def forward(self, x):
        features_enconder1, down = self.encoder1(x)
        features_enconder2, down = self.encoder2(down)
        features_enconder3, down = self.encoder3(down)
        features_enconder4, down = self.encoder4(down)
        features_bottom, _ = self.encoder_bottom(down)

        x = self.decoder4(features_enconder4, features_bottom)
        x = self.decoder3(features_enconder3, x)
        x = self.decoder2(features_enconder2, x)
        x = self.decoder1(features_enconder1, x)
        x = self.outConv(x)

        return x
