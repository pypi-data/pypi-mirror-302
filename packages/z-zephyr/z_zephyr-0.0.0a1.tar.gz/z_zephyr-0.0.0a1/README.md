# zephyr

![Work in Progress](https://img.shields.io/badge/work%20in%20progress-purple)
![Early Stage](https://img.shields.io/badge/stage-early-yellow)

NOTE: Work in progress; enough to demonstrate the core feature; very early stage

[Summary](#summary) | [Core Principle](#core) | [Example: Autoencoder](#autoencoder) | [Example: Linear](#linear) | [Motivation and Inspiration](#motivation)

## Summary<a id="summary"></a>
The [JAX](https://github.com/jax-ml/jax) library offers most things that you need for making neural networks, but there is no 
shortage of frameworks/libraries that build on JAX to cater to neural net building. 


zephyr focuses on 2 things:
- **Parameter Creation**. The number one pain point for using jax for neural networks is the difficulty of the laborious and tedious process of creating the parameters
- **Simplicity**. Neural networks are pure functions, but none of the frameworks present neural network as such pure functions. They always treat a neural network as something extra which is why you would need some special methods or transforms or re-duplicated jax methods.

## Core Principle<a id="core"></a>
A neural network $f$ is simply mathematical function of data $X$, parameters $\theta$, and hyper-parameters $\alpha$. We place $\theta$ as the first parameter of $f$ because `jax.grad` creates the gradient of $f$ wrt to the first parameter by default.

$$ f(\theta, X, \alpha) $$

## Examples
Here are two examples to demonstrate and highlight what zephyr empowers: simplicity, and control.

### Making an autoencoder<a id="autoencoder"></a>
Let's make a simple autoencoder. The encoder will use 2 mlp's in succession and the decoder will use just 1. 
```python
from zephyr._nets.mlp import mlp
def encoder(params, x, embed_dim, latent_dim):
    x = mlp(params["mlp_1"], x, [embed_dim, embed_dim])
    x = mlp(params["mlp_2"], x, [embed_dim, latent_dim])
    return x

def decoder(params, x, embed_dim, original_dim):
    x = mlp(params, x, [embed_dim, embed_dim, latent_dim])
    return x

def autoencoder(params, x, embed_dim, latent_dim):
    encoding = encoder(params["encoder"], x, embed_dim, latent_dim)
    reconstruction = decoder(params["decoder"], x, embed_dim, x.shape[-1])

    return reconstruction
```

Notice that we named `params` whenever it was passed to the encoder mlp: `params["mlp_1]` and `params["mlp_2"]`. 
These names are essential and is part of zephyr's design to allow maximum control over all parameters. 

Notice that an `mlp` is not some object, not some function passed to a transform, not a dataclass PyTree object, it is simply
a function `mlp(params, x, num_out_per_layer)`. There is no need to instatiate a model or a neural network. It's just a function! 
(Later we will show more reasons why this would be advantageous)

We have an autoencoder, now how do we instatiate the model? As said before, no instatiation needed. What we do need is a an initial
`params`. This is easy with the `trace` function.
```python
from zephyr.building.tracing import trace
from jax import random

batch_size = 8
initial_dim = 64
latent_dim = 256
embed_dim = 512

key = random.PRNKey(0)
x = jnp.ones([batch_size, initial_dim]) # this is a sample input

params = trace(autoencoder, key, x, embed_dim, latent_dim)

"""
params = {
    encoder: {
        mlp_1: {weights: ..., biases: ...},
        mlp_2: {weight: ..., biases: ...}
    },
    decoder: {
        weights: ...,
        biases: ...
    }
}
"""
```

Notice how each of the entries in `params` were appropriately named. This would be automatic in some frameworks, but having explicit names 
allows us to take apart the model with ease as we will see below.

```python
# assume you are done training and params contained trained weights (use another library like optax for this)

# what if you want to use just the encoder?
encodings = encoder(params["encoder"], x, embed_dim, latent_dim)

# what you want to use just the decoder?
some_reconstructions = decoder(params["decoder"], encodings, embed_dim, x.shape[-1])

# what if you want to just use the mlp_2 in encoder?
mlp(params["encoder"]["mlp_2"], some_input, [embed_dim, latent_dim])

# what if you want to be silly and make an encoder with mlp_1 and mlp_2 flipped and still use the encoder's weights?
def flipped_encoder(params, x, embed_dim, latent_dim):
    x = mlp(params["mlp_2"], x, [embed_dim, latent_dim])
    x = mlp(params["mlp_1"], x, [embed_dim, embed_dim])
    return x

# and use the flipped_encoder trivially as this
encoding_of_flipped_encoder = flipped_encoder(params["encoder"], x, embed_dim, latent_dim)
```

As you can see, by being on the jax-level all the time, you are free to do whatever you want. Coding becomes short and to the point. 

### Building Layers From Scratch<a id="linear"></a>
Usually it is rare that one would need to instantiate their own trainable weights (specifying the shape and initializer) since Linear / MLP layers usually suffice for that. Frameworks usually differ in how to handle parameter building and it is part of what makes the core
experience in these frameworks. This part is also where clever things in each framework is hidden. For zephyr, it wanted to keep 
functions pure, but parameter building is hard. To make it easier zephyr had to rely on python's quirkyness. 

Let's implement the linear layer from scratch.
```python
from zephyr.building import initializers, template 

def linear(
    params: PyTree,
    x: Array,
    target_out: int,
    with_bias: bool = True,
    initializer=initializers.initializer_base,
) -> Array:
    params["weights"] == template.array((target_out, x.shape[-1]), initializer)
    z = jnp.expand_dims(x, axis=-1)
    z = params["weights"] @ z
    z = jnp.squeeze(z, axis=-1)

    if with_bias:
        params["bias"] == template.array((target_out,), initializer)
        z = params["bias"] + z

    return z
```
The key part are where `params["name_of_params"]` is `==` to a template that contains the shape information and the initializer information. This tells the `trace` function how to initialize these weights. These statements also provide typing-like statement which tells you
what template that parameter follows before using it. 

And as seen, earlier, to use this, just use the `trace` function.

```python
from jax import numpy as jnp, random

key = random.PRNKey(0)
dummy_inputs = jnp.ones([64, 8])
params = trace(linear, key, dummy_inputs, 128)

sample_outputs = linear(params, dummy_inputs, 128) # shape: [64, 128]
```


## Motivation and Inspiration<a id="motivation"></a>
This library is heavily inspired by [Haiku](https://github.com/google-deepmind/dm-haiku)'s `transform` function which eventually
converts impure functions/class-method-calls into a pure function paired with an initilized `params` PyTree. This is my favorite 
approach so far because it is closest to pure functional programming. Zephyr tries to push this to the simplest and make neural networks 
simply just a function. 

This library is also inspired by other frameworks I have tried in the past: Tensorflow and PyTorch. Tensorflow allows for shape
inference to happen after the first pass of inputs, PyTorch (before the Lazy Modules) need the input shapes at layer creation. Zephyr 
wants to be as easy as possible and will strive to always use at-inference-time shape-inference and use relative axis positions whenever possible. 




