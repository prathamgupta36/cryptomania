## Preimage Resistance

This challenge demonstrates how weak a hash becomes when its output is truncated too aggressively. The target digest is only 3 bytes of SHAKE256 output, so finding a matching preimage is practical.

Submit any hex-encoded message whose SHAKE256 digest matches the target value shown by the service.
