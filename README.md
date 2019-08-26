# AG-LayCast
## What's this repository?
This repository contains four datasets ([Twitch trace](https://clivecast.github.io/), [4G/LTE Bandwidth Logs](https://users.ugent.be/~jvdrhoof/dataset-4g/), [GPS trajectory](https://www.microsoft.com/en-us/download/details.aspx?id=52367) and [BS\AP locatioon](https://github.com/darcy-shimmer/AG-LayCast/tree/master/BS-AP-locatioon)), simulation codes and other two repositories ([srs](https://github.com/ossrs/srs) and [yasea](https://github.com/begeekmyfriend/yasea)) for prototype implementation.

## Preparation
> git clone https://github.com/darcy-shimmer/AG-LayCast.git

### Build srs
> cd AG-LayCast/srs/trunk
> ./configure --with-ssl --with-http-api --with-hls --with-http-server --with-nginx --with-ffmpeg --with-transcode && make

## Usage
