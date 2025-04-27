def calculate_slope(values):
    return (values[-1] - values[0]) / (len(values) - 1)

def influence_index(gen_z, older):
    m_g = calculate_slope(gen_z)
    m_o = calculate_slope(older)

    if m_o == 0:
        return 0.0

    if m_g == 0:
        # Gen Z is flat, older gens rising or falling
        return m_o  # influence = slope of older gens

    if (m_g > 0 and m_o > 0) or (m_g < 0 and m_o < 0):
        # Aligned trends
        return m_o / m_g
    else:
        # Opposite trends
        return -abs(m_o / m_g)


# --------------------------
# User Input Section
# --------------------------

n = int(input("Enter number of data points (years): "))

print(f"Enter {n} values for Gen Z, separated by spaces:")
gen_z = list(map(float, input().strip().split()))

print(f"Enter {n} values for Older Generations, separated by spaces:")
older = list(map(float, input().strip().split()))

if len(gen_z) != n or len(older) != n:
    print("Error: Number of inputs does not match expected count.")
else:
    index = influence_index(gen_z, older)
    print(f"\n📊 Influence Index: {index}")


# # -------------------
# # TEST CASES
# # -------------------

# tests = [
#     # Gen Z flat at 80%, older gens rise from 10 → 60 (strong convergence)
#     ([80, 80, 80], [10, 35, 60]),

#     # Gen Z flat at 80%, older gens rise from 10 → 20 (small convergence)
#     ([80, 80, 80], [10, 15, 20]),

#     # Gen Z flat at 80%, older gens decline from 60 → 20 (diverging)
#     ([80, 80, 80], [60, 40, 20]),

#     # Gen Z rising fast, older gens flat
#     ([20, 30, 50], [10, 10, 10]),

#     # Gen Z declining, older gens declining
#     ([70, 60, 50], [30, 20, 10]),

#     # Both rising moderately
#     ([60, 65, 70], [10, 15, 20]),

#     # Moderate increase, both
#     ([47, 53, 57], [29, 32, 36]),

#     # Subtle increase
#     ([62, 65, 68], [58, 60, 64.7]),

#     # Gen Z rising strongly, older gens catching up
#     ([90, 95, 96.4], [64.68, 80, 90]),

#     # Gen Z declining, older gens rising — opposing trends
#     ([23.9, 25, 20.98], [18.79, 16.56, 22.58])
# ]

# print("Influence Index Results:")
# for i, (gen_z, older) in enumerate(tests, 1):
#     result = influence_index(gen_z, older)
#     print(f"{i}. Influence Index = {result}")







# import numpy as np

# def influence_index(gen_z, older, years=[2015, 2020, 2025]):
#     # Compute slopes
#     m_G = (gen_z[2] - gen_z[0]) / (years[2] - years[0])
#     m_O = (older[2] - older[0]) / (years[2] - years[0])

#     # Distance at start and end
#     d_start = abs(gen_z[0] - older[0])
#     d_end = abs(gen_z[2] - older[2])
    
#     # Avoid division by zero
#     factor = (d_end - d_start) / d_start if d_start != 0 else 0

#     # Case 1: Older flat — no influence
#     if m_O == 0:
#         return 0

#     # Case 2: Gen Z flat — use convergence to scale upward or penalize decline
#     if m_G == 0:
#         return m_O * (1 - factor) if m_O > 0 else m_O * (1 + abs(factor))

#     # Case 3: Trends aligned (both rising or both falling)
#     if np.sign(m_G) == np.sign(m_O):
#         return m_O * (1 - factor)

#     # Case 4: Opposite trends — penalize heavily
#     return m_O * (1 + abs(factor)) * -1


# print(influence_index([80, 80, 80], [10, 35, 60]))  # High positive
# print(influence_index([80, 80, 80], [10, 15, 20]))  # Small positive
# print(influence_index([80, 80, 80], [60, 40, 20]))  # Negative
# print(influence_index([20, 30, 50], [10, 10, 10]))  # 0
# print(influence_index([70, 60, 50], [30, 20, 10]))  # Aligned decline
# print(influence_index([60, 65, 70], [10, 15, 20]))  # Positive
# print(influence_index([47, 53, 57], [29, 32, 36]))  # Mild positive
# print(influence_index([62, 65, 68], [58, 60, 64.7])) # Medium
# print(influence_index([90, 95, 96.4], [64.68, 80, 90]))  # High
# print(influence_index([23.9, 25, 20.98], [18.79, 16.56, 22.58]))  # Negative cia civi participation Lithuania
