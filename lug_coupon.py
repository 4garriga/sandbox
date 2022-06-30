import matplotlib as mpl
import matplotlib.pyplot as plt 
from numpy import cos, sin, pi, arange 

h, x0, y0, r0 = 3, 2, 1.5, 1.5 
xi, yi, ri = 2.75, 1.75, 0.50
th = 0.75 
theta = arange(-pi/2, pi/2 + pi/180, pi/180)
fig, ax = plt.subplots()
ax.plot(
    x0 + r0*cos(theta), y0 + r0*sin(theta), 'k-',
    [x0, 0, 0, x0], [h, h, 0, 0], 'k-',
    x0, y0, 'k+',
    xi, yi, 'k+',
    xi + ri*cos(arange(0, 2*pi, pi/180)), yi + ri*sin(arange(0, 2*pi, pi/180)), 'k-',
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
s = -0.1
ax.annotate(
    '',
    xy=(s, y0),
    xytext=(s, 0),
    arrowprops={
        'arrowstyle': '->',
        },
    )
ax.text(s, y0, 'y0', ha='center')
ax.annotate(
    '',
    xy=(x0, s),
    xytext=(0, s),
    arrowprops={
        'arrowstyle': '->',
        })
ax.text(x0, s, 'x0', va='center')

dx = dy = 0.1
ax.plot([dx, x0 - dx], [y0, y0], 'k-',)  # y
ax.plot([dx, xi - dx], [yi, yi], 'k-',)
ax.plot([x0, x0], [dy, y0 - dy], 'k-',)  # x 
ax.plot([xi, xi], [dy, yi - dy], 'k-',)

# r0 
a = pi/6
ax.annotate(
    '',
    xy=(x0 + r0*cos(a), y0 + r0*sin(a)),
    xytext=(x0, y0),
    arrowprops={
        'arrowstyle': '->',
        }
        )
ax.text(x0 + r0*cos(a), y0 + r0*sin(a), 'r0')

# xi, yi 
s = -0.2 
ax.annotate(
    '',
    xy=(s, yi),
    xytext=(s, 0),
    arrowprops={
        'arrowstyle': '->',
        },
    )
ax.text(s, yi, 'yi', ha='center')
ax.annotate(
    '',
    xy=(xi, s),
    xytext=(0, s),
    arrowprops={
        'arrowstyle': '->',
        })
ax.text(xi, s, 'xi', va='center')

# ri 
# a = pi/6
ax.annotate(
    '',
    xy=(xi + ri*cos(a), yi + ri*sin(a)),
    xytext=(xi, yi),
    arrowprops={
        'arrowstyle': '->',
        }
        )
ax.text(xi + ri*cos(a), yi + ri*sin(a), 'ri')

# Height 
s = -0.30
ax.annotate(
    '',
    xy=(s, h),
    xytext=(s, 0),
    arrowprops={
        'arrowstyle': '->',
        })
ax.text(s, h, 'h', ha='center')

# Thickness
s = -0.45
ax.plot(
    [s, s, s - th, s - th, s],
    [0, h, h, 0, 0], 'k-',)
ax.annotate(
    '',
    xy=(s, h + 0.1),
    xytext=(s - th, h + 0.1),
    arrowprops={
        'arrowstyle': '<->',
        })
ax.text(-th/2 + s, h + 0.15, 'th')
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
plt.ylim((-0.3, top))
plt.axis('off')
fig.tight_layout()
fig.show()
plt.savefig('lug-coupon.png')

