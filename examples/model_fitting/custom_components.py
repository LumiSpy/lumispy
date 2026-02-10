"""
Create Custom Components
========================
In this example, we will show you how to create custom components.

.. _HS_create_components: https://hyperspy.org/hyperspy-doc/current/user_guide/model/model_components.html#define-components-from-a-mathematical-expression
.. _HS_fixed-pattern: https://hyperspy.org/hyperspy-doc/current/reference/api.model/components1D.html#hyperspy.api.model.components1D.ScalableFixedPattern
"""

# %%
# First we will create a signal.
import hyperspy.api as hs
import numpy as np

x = np.linspace(-50, 50, 500)
y = np.power(x, 2) + np.random.normal(0, 100, x.shape)
s = hs.signals.Signal1D(y)
m1 = s.create_model()
m2 = s.create_model()

axis = s.axes_manager[-1]
axis.name = "x"
axis.scale = x[1] - x[0]
axis.offset = x[0]

# %%
# Mathematical Expression
# -----------------------
#
# We can create a custom component using a mathematical expression.
g1 = hs.model.components1D.Expression(expression="a * x**2 + b", name="Quadratic")
m1.append(g1)
m1.fit()
m1.plot()

# %%
# Define from a function
# ----------------------
#
# You can define more general components modifying the following template[#f1]_:
from hyperspy.component import Component


class MyComponent(Component):
    def __init__(self, p1=1, p2=2):
        Component.__init__(self, ("p1", "p2"))

        # Optionally we can set the initial values
        self.p1.value = p1
        self.p2.value = p2

    # Define the function as a function of the already defined paramters,
    # x being the independent vaiable value
    def function(self, x):
        return self.p1.value * x**2 + self.p2.value


g2 = MyComponent()
m2.append(g2)
m2.fit()
m2.plot()

# %%
# Define from a fixed-pattern
# ---------------------------
#
# The ``ScalableFixedPattern`` component, enables fitting a pattern (in the form of a ``Signal1D`` instance) to data by shifting (``shift``) and scaling it in the x and y directions using
# the ``xscale`` and ``yscale`` parameters respectively, see more in the `docs <HS_fixed-pattern_>`__.
data = hs.signals.Signal1D(np.power(x, 2))
m3 = s.create_model()
fixed_pattern = hs.model.components1D.ScalableFixedPattern(s)
m3.append(fixed_pattern)
m3.fit()
m3.plot()

# %%
# sphinx_gallery_thumbnail_number = 4
#
# .. [#f1] To learn more about creating custom components, check out the `Hyperspy documentation <HS_create_components_>`__.
