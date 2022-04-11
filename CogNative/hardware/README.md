# Hardware / Performance
Prototype hardware due to availability and issues with initial selection is a Windows 10 PC. There may be multiple viable hardware solutions for a commercial product in different price tiers with different performance targets than the maximum capabilities of our prototype hardware. 

## Prototype Specifications Evaluation (As of 4 Apr '22)

### CPU: i7 3770 (3.4GHz, 4C/8T)
Testing with single-sentence job, CPU load increased by 15%, indicating that it's not currently a limiting factor.

### RAM: 24GB DDR3
1.5GB peak consumed by process during encoding step, indicating capacity is unlikely to become a limiting factor.

### GPU: MSI GTX 980 Gaming 4G
Peak memory consumption about 2.2GB during processing of short audio file "MatthewM66.wav" but longer files, while producing better quality, require more memory or possibly being split into segments. Improvements to processing quality could exceed the dedicated memory of the GPU and cause slowdowns as it is forced to swap to shared system memory, or cause crashes if the ultimate limit is exceeded. 

Peak GPU core load was 10%, indicating it's not currently a limiting factor.

## Prototype Performance

Since neither CPU, GPU, nor RAM reported high utilization, there is some other factor limiting performance. The natural assumption is I/O, but further investigation is required for maximizing performance. We plan to investigate mitigations for the possibility of ballooning GPU memory usage. 

## Recommended Specifications 

### With dedicated Nvidia GPU
GPU should have 4GB of dedicated memory for acceptable performance, but more is preferable.
Any modern x86 CPU with around 2-4GB of free RAM should suffice for current performance.
### Without dedicated GPU
Performance suffers in CPU mode; to meet the same performance target would require an unknown amount more than a Ryzen 3700x. 
