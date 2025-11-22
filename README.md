# Progress Report – Pilgrimage Itinerary Generator
## 1. Summary
Initial analysis of the Itinerary Generator project is complete. Two backend approaches were explored. One has been rejected; the other is currently under development.

---

## 2. Requirements Understood
User selects:
- **1 Pandit**
- **3 Temples**
- **1 Lunch Spot**

System must:
- Generate a full itinerary
- Display locations on a map (markers + route)
- Provide an AI-generated summary
- Work end-to-end on localhost

---

## 3. Approach Evaluation

### **Approach 1: Scheduling-Based Algorithm (Rejected)**
Attempted modeling temple visits similar to OS scheduling tasks.

**Reasons for Rejection:**
- Unpredictable visit durations  
- Temples are not exclusive resources (many people can visit at once)  
- Inability to estimate crowd/traffic reliably  
- Adds unnecessary computational complexity  

---

### **Approach 2: Coordinate + Route Optimization (In Progress)**
- Storing latitude and longitude for all locations  
- Utilizing mapping APIs for route and travel-time estimation  
- Building itinerary based on geographic proximity  

**Reason for Selection:**  
This approach is more practical, scalable, and aligns with real-world travel systems.

**Status:** Currently being implemented.

---


