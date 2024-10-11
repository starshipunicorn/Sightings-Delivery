import streamlit as st
import requests

# Discord webhook URL (replace with your own webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1272625772577951856/bzwIwPK6IYTPmhlD6bcLoB2thA0ha-I9nIgn1SNV-J1yTvIA59a7NVAgseSouduAUguU"

# Menu Items with their Prices
menu = {
    "Breakfast": {
        "Crater Cinnamon Roll Pancakes": 73.50,
        "Nebula Nosh Chicken & Waffles": 115.50,
        "Extraterrestrial Omelet": 87.50
    },
    "Starters": {
        "Celestial Caesar Salad": 70.00,
        "Alien Antenna Bites": 98.00,
        "Orbiting Onion Rings": 52.50
    },
    "Mains": {
        "Celestial Creature Gyro": 115.50,
        "Andromeda Invader Curry": 105.00,
        "Planetary Pizza": 70.00,
        "Galaxy Guac Burger and Meteorite Fries": 122.50
    },
    "Desserts": {
        "Spacecraft S’mores Shake": 950,
        "Blackhole Brownies": 66.50,
        "Martian Mousse": 73.50
    },
    "Alcoholic Drinks": {
        "UFO Umbrella Drink": 50.00,
        "Asteroid Amaretto Sour": 57.50,
        "Alien Ambrosia": 62.50
    },
    "Non-Alcoholic Drinks": {
        "Lunar Lemonade": 27.50,
        "Comet Cola Float": 32.50,
        "Galactic Grape Cola": 27.50,
        "Nebula Nectar Cola": 27.50
    }
}

# Function to calculate total price
def calculate_total(order):
    subtotal = 0
    for item, quantity in order.items():
        subtotal += menu[item[0]][item[1]] * quantity

    delivery_fee = 200
    total = subtotal + delivery_fee

    return round(subtotal, 2), round(total, 2)

# Function to send order to Discord
def send_order_to_discord(phone_number, delivery_location, order_summary, total_price):
    data = {
        "content": f"New Order Received:\n\nPhone Number: {phone_number}\nDelivery Location: {delivery_location}\n\n{order_summary}\n**Total: ${total_price}**"
    }
    response = requests.post(WEBHOOK_URL, json=data)
    return response.status_code == 204

# Streamlit Interface
st.title("🚀 Sightings Delivery 🌌")

# Section for entering in-character phone number
phone_number = st.text_input("Enter your in-character phone number", "")

# Section for entering delivery location
delivery_location = st.text_input("Delivery Location", "")

order = {}

cols = st.columns(2)

# First row
with cols[0]:
    st.subheader("🌅 Breakfast")
    for item, price in menu["Breakfast"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Breakfast", item)] = quantity

with cols[1]:
    st.subheader("🍲 Starters")
    for item, price in menu["Starters"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Starters", item)] = quantity

# Second row
cols = st.columns(2)

with cols[0]:
    st.subheader("🍽️ Mains")
    for item, price in menu["Mains"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Mains", item)] = quantity

with cols[1]:
    st.subheader("🍰 Desserts")
    for item, price in menu["Desserts"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Desserts", item)] = quantity

# Third row
cols = st.columns(2)

with cols[0]:
    st.subheader("🍹 Alcoholic Drinks")
    for item, price in menu["Alcoholic Drinks"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Alcoholic Drinks", item)] = quantity

with cols[1]:
    st.subheader("🥤 Non-Alcoholic Drinks")
    for item, price in menu["Non-Alcoholic Drinks"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Non-Alcoholic Drinks", item)] = quantity

if st.button("Submit Order"):
    subtotal, total_price = calculate_total(order)
    delivery_fee = 200
    order_summary = "\n".join([f"- {item} ({category}): {quantity} @ ${menu[category][item]} each"
                               for (category, item), quantity in order.items()])
    
    st.markdown(f"## Subtotal: **${subtotal}**")
    st.markdown(f"### Delivery Fee: **${delivery_fee}**")
    st.markdown(f"## 🧾 The total price of the order is: **${total_price}**")
    
    st.subheader("Order Summary")
    st.markdown(order_summary)

    if send_order_to_discord(phone_number, delivery_location, order_summary, total_price):
        st.success("Order sent successfully to Sightings!")
    else:
        st.error("Failed to send order to Sightings.")
