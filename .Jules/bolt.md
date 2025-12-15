## 2025-12-11 - Mathematical Identity Optimization
**Learning:** Sometimes complex functions effectively calculate the identity (e.g., Forward Dynamics followed by Inverse Dynamics). Recognizing this allows replacing O(N) expensive operations with O(1) assignment.
**Action:** Always check if a sequence of operations is mathematically circular (A -> B -> A) and simplify if possible.
