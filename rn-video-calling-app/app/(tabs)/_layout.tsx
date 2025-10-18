import { Tabs } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <>
      <StatusBar style="light" />
      <Tabs
        screenOptions={{
          headerStyle: { backgroundColor: "#fce7f3" },
          headerTintColor: "#374151",
          headerTitleAlign: "center",
          tabBarStyle: { 
            backgroundColor: "#fce7f3",
            borderTopColor: "#f9a8d4",
            borderTopWidth: 1,
          },
          tabBarActiveTintColor: "#ec4899",
          tabBarInactiveTintColor: "#6b7280",
        }}
      >
        <Tabs.Screen
          name="index"
          options={{ 
            title: "Date",
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="heart" size={size} color={color} />
            ),
            headerTitle: "AuraDate"
          }}
        />
        <Tabs.Screen
          name="spark"
          options={{ 
            title: "Spark",
            tabBarIcon: ({ color, size}) => (
              <Ionicons name="people" size={size} color={color} />
            ),
            headerTitle: "Conversation Spark"
          }}
        />
        <Tabs.Screen
          name="profile"
          options={{ 
            title: "Profile",
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="person" size={size} color={color} />
            ),
            headerTitle: "Profile"
          }}
        />
      </Tabs>
    </>
  );
}
