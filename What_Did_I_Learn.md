# What Did I Learn?

This assignment helped me understand how Django models can be used to solve a practical warehouse problem by storing product details, order quantities, and box capacities.

I learned that checking only the total volume is not enough to determine whether products fit inside a box. The application also needs to consider product dimensions, possible rotations, overlapping products, and the total weight of the order.

I also understood the importance of testing different scenarios, especially when product weights change or a box cannot support the total order weight. Writing tests helped me understand how to verify the recommendation logic and identify bugs.