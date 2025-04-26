import numpy as np
import matplotlib.pyplot as plt

num_groups = 5
num_points = 10
max_deviation = 1.5

central_points = np.random.uniform(0, 20, (num_groups, 2))

points = []
for cx, cy in central_points:
    x_offsets = np.random.uniform(-max_deviation, max_deviation, num_points)
    y_offsets = np.random.uniform(-max_deviation, max_deviation, num_points)
    group_points = np.column_stack((cx + x_offsets, cy + y_offsets))
    points.append(group_points)

group_means = [np.mean(group, axis=0) for group in points]
group_max_devs = [np.max(np.abs(group - mean), axis=0) for group, mean in zip(points, group_means)]

plt.figure(figsize=(8, 6))
colors = ['r', 'g', 'b', 'm', 'c']
markers = ['o', 's', 'D', '^', 'v']

for i, (group, mean, max_dev, color, marker) in enumerate(zip(points, group_means, group_max_devs, colors, markers)):
    x, y = group[:, 0], group[:, 1]
    plt.scatter(x, y, color=color, alpha=0.6, marker=marker, label=f'Группа {i+1}')
    plt.errorbar(mean[0], mean[1], xerr=max_dev[0], yerr=max_dev[1], fmt='o', color=color, capsize=5, markersize=8)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('График с учетом погрешностей')
plt.legend()
plt.grid(True)
plt.show()
