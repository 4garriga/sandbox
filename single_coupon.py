import matplotlib as mpl
import matplotlib.pyplot as plt 
from numpy import cos, sin, pi, arange 

d = 1.0
w, h = 8*d, 4*d
x0, y0 = w/2, h/2
th = 0.75 
theta = arange(0, 2*pi, pi/180)

fig, ax = plt.subplots()
dx, dy = 0.1, 0.1
ax.plot(
    [0, w, w, 0, 0], [0, 0, h, h, 0], 'k-',
    x0 + d/2*cos(theta), y0 + d/2*sin(theta), 'k-',
    [dx, x0 - dx], [y0, y0], 'k-',
    [x0, x0], [dy, y0 - dy], 'k-',
    x0, y0, 'k+',
    )

# Origin 
ax.annotate(
    "",
    xy=(0.5, 0),
    xytext=(0, 0),
    arrowprops={
        'arrowstyle': '->',
        },
    )
ax.text(0.5, 0.05, 'x', va='center')
ax.annotate(
    "",
    xy=(0, 0.5),
    xytext=(0, 0),
    arrowprops={
        'arrowstyle': '->',
        },
    )
ax.text(0.05, 0.5, 'y', ha='center')

# x0, y0
s = -0.15
ax.annotate(
    '',
    xy=(x0, s),
    xytext=(0, s),
    arrowprops={
        'arrowstyle': '->',
        },
    )
ax.text(x0, s, 'x0', va='center')
ax.annotate(
    '',
    xy=(s, y0),
    xytext=(s, 0),
    arrowprops={
        'arrowstyle': '->',
        })
ax.text(s, y0, 'y0', ha='center')

# Width 
s = -0.30
ax.annotate(
    '',
    xy=(w, s),
    xytext=(0, s),
    arrowprops={
        'arrowstyle': '->',
        })
ax.text(w, s, 'w', va='center')

# Height 
ax.annotate(
    '',
    xy=(s, h),
    xytext=(s, 0),
    arrowprops={
        'arrowstyle': '->',
        })
ax.text(s, h, 'h', ha='center')
        
# D 
a = pi/4
a1 = a - pi 
ax.annotate(
    '',
    xy=(x0 + d/2*cos(a), y0 + d/2*sin(a)),
    xytext=(x0 + d/2*cos(a1), y0 + d/2*sin(a1)),
    arrowprops={
        'arrowstyle': '<->',
        },
    )
ax.text(x0 + d/2*cos(a), y0 + d/2*sin(a), 'D')
# Thickness
s = -0.50
ax.plot([s, s, s - th, s - th, s], [0, h, h, 0, 0], 'k-')
ax.annotate(
    '',
    xy=(s, h + 0.1),
    xytext=(s - th, h + 0.1),
    arrowprops={
        'arrowstyle': '<->',
        })
ax.text(-th/2 + s, h + 0.15, 'th', ha='center') 
ax.annotate(  # z-axis
    "",
    xy=(s - th + 0.5, 0),
    xytext=(s - th, 0),
    arrowprops={
        'arrowstyle': '->',
        },
    )
ax.text(s - th + 0.5, 0.05, 'z', va='center')
ax.annotate(
    "",
    xy=(s - th, 0.5),
    xytext=(s - th, 0),
    arrowprops={
        'arrowstyle': '->',
        },
    )
ax.text(s - th + 0.05, 0.5, 'y', ha='center')

# Show 
ax.axis('equal')
bot, top = plt.ylim()
# plt.ylim((-0.3, top))
plt.axis('off')
fig.tight_layout()
fig.show()
fig.savefig('single-coupon.png')