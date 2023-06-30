# Caterpillar Code-a-thon 2023
----
# Color Pattern Sequence Frame Detector 
Develop a solution to analyze the incoming video stream of color patterns and identify each color and their duration and correct sequence. Based on the available list of known sequence patterns, identify the start and end of full or partial patterns in the stream.

# Deliverables and tools that can be used
1. Leverage existing Python libraries to capture the live video stream from a PC camera.
2. Identify the major color on stream and decode based on the RGB values
3. Measure the duration of each color slot and create a sequence based on the shortest color slot duration.
4. Compare the continuous stream/sequence with the available list of patterns and identify the start and end of full/partial/invalid pattern
