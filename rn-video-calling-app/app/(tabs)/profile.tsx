import { useState, useEffect } from "react";
import { View, Text, TextInput, Pressable, Switch, Alert, ScrollView, ActivityIndicator } from "react-native";
import { Ionicons } from '@expo/vector-icons';
import { useDisplayName } from '@/hooks/useDisplayName';
import { API_BASE_URL } from '@/config/api';

export default function ProfileScreen() {
  const { displayName, setDisplayName, isLoading } = useDisplayName();
  const [name, setName] = useState(displayName);
  const [fullName, setFullName] = useState("");
  const [linkedInUrl, setLinkedInUrl] = useState("");
  const [instagramUsername, setInstagramUsername] = useState("");
  const [twitterUsername, setTwitterUsername] = useState("");
  const [email, setEmail] = useState("abel@example.com");
  const [bio, setBio] = useState("AI Study Assistant");
  const [notifications, setNotifications] = useState(true);
  const [micEnabled, setMicEnabled] = useState(true);
  const [cameraEnabled, setCameraEnabled] = useState(true);
  const [avatarEnabled, setAvatarEnabled] = useState(true);
  const [isScraping, setIsScraping] = useState(false);

  // Sync local state with stored display name
  useEffect(() => {
    if (!isLoading && displayName) {
      setName(displayName);
    }
  }, [displayName, isLoading]);

  const handleSave = async () => {
    try {
      // First update the display name
      await setDisplayName(name);
      
      // If LinkedIn URL, full name, or any social media fields are filled, scrape and update profile
      const hasSocialMedia = linkedInUrl.trim() || instagramUsername.trim() || twitterUsername.trim();
      
      if (hasSocialMedia || (fullName.trim() && fullName !== name)) {
        setIsScraping(true);
        
        try {
          const response = await fetch(`${API_BASE_URL}/api/update-user-profile`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              display_name: name,
              full_name: fullName || name,
              linkedin_url: linkedInUrl.trim() || null,
              instagram_username: instagramUsername.trim() || null,
              twitter_username: twitterUsername.trim() || null,
              include_facebook: true,  // Always include Facebook scraping
            }),
          });
          
          if (!response.ok) {
            throw new Error('Failed to update profile with social media data');
          }
          
          const result = await response.json();
          
          Alert.alert(
            "Profile Updated! 🎉", 
            `Your profile has been saved successfully!\n\n${result.profiles_scraped > 0 
              ? `✓ Scraped ${result.profiles_scraped} social media profile(s)\n✓ Added context to your dating AI` 
              : 'Profile information saved'}`
          );
        } catch (error) {
          console.error('Error scraping social media:', error);
          Alert.alert(
            "Profile Saved",
            "Your basic profile was saved, but we couldn't scrape your social media. Please check your information and try again."
          );
        } finally {
          setIsScraping(false);
        }
      } else {
        Alert.alert("Profile Updated", "Your profile has been saved successfully!");
      }
    } catch (error) {
      Alert.alert("Error", "Failed to save profile. Please try again.");
    }
  };

  return (
    <ScrollView className="flex-1 bg-pink-50">
      <View className="px-5 py-6">
        {/* Profile Header */}
        <View className="items-center mb-8">
          <View className="w-24 h-24 rounded-full bg-pink-600 items-center justify-center mb-4">
            <Ionicons name="person" size={40} color="white" />
          </View>
          <Text className="text-gray-800 text-2xl font-semibold">{name}</Text>
          <Text className="text-gray-600 text-base">{email}</Text>
        </View>

        {/* Basic Information */}
        <View className="mb-6">
          <Text className="text-gray-800 text-lg font-semibold mb-4">Basic Information</Text>
          
          <View className="mb-4">
            <Text className="text-gray-700 mb-2">Display Name</Text>
            <TextInput
              value={name}
              onChangeText={setName}
              placeholder="Enter your name"
              placeholderTextColor="#6b7280"
              className="border border-gray-300 rounded-xl px-4 py-3 text-gray-800 bg-white"
            />
          </View>

          <View className="mb-4">
            <Text className="text-gray-700 mb-2">Full Name</Text>
            <TextInput
              value={fullName}
              onChangeText={setFullName}
              placeholder="Enter your full name"
              placeholderTextColor="#6b7280"
              className="border border-gray-300 rounded-xl px-4 py-3 text-gray-800 bg-white"
            />
          </View>

          <View className="mb-4">
            <Text className="text-gray-700 mb-2">Email</Text>
            <TextInput
              value={email}
              onChangeText={setEmail}
              placeholder="Enter your email"
              placeholderTextColor="#6b7280"
              className="border border-gray-300 rounded-xl px-4 py-3 text-gray-800 bg-white"
              keyboardType="email-address"
            />
          </View>

          <View className="mb-4">
            <Text className="text-gray-700 mb-2">Bio</Text>
            <TextInput
              value={bio}
              onChangeText={setBio}
              placeholder="Tell us about yourself"
              placeholderTextColor="#6b7280"
              className="border border-gray-300 rounded-xl px-4 py-3 text-gray-800 bg-white"
              multiline
              numberOfLines={3}
            />
          </View>
        </View>

        {/* Social Media */}
        <View className="mb-6">
          <Text className="text-gray-800 text-lg font-semibold mb-4">Social Media</Text>
          
          <Text className="text-gray-600 text-sm mb-4">
            Add your LinkedIn URL to get professional context. We'll also find your Facebook using your full name!
          </Text>

          <View className="mb-4">
            <Text className="text-gray-700 mb-2">LinkedIn URL</Text>
            <TextInput
              value={linkedInUrl}
              onChangeText={setLinkedInUrl}
              placeholder="https://linkedin.com/in/username"
              placeholderTextColor="#6b7280"
              className="border border-gray-300 rounded-xl px-4 py-3 text-gray-800 bg-white"
              keyboardType="url"
              autoCapitalize="none"
            />
          </View>

          <View className="mb-4">
            <Text className="text-gray-700 mb-2">Instagram Username</Text>
            <TextInput
              value={instagramUsername}
              onChangeText={setInstagramUsername}
              placeholder="@username"
              placeholderTextColor="#6b7280"
              className="border border-gray-300 rounded-xl px-4 py-3 text-gray-800 bg-white"
              autoCapitalize="none"
            />
          </View>

          <View className="mb-4">
            <Text className="text-gray-700 mb-2">Twitter/X Username</Text>
            <TextInput
              value={twitterUsername}
              onChangeText={setTwitterUsername}
              placeholder="@username"
              placeholderTextColor="#6b7280"
              className="border border-gray-300 rounded-xl px-4 py-3 text-gray-800 bg-white"
              autoCapitalize="none"
            />
          </View>
        </View>

        {/* Call Settings */}
        <View className="mb-6">
          <Text className="text-gray-800 text-lg font-semibold mb-4">Call Settings</Text>
          
          <View className="flex-row items-center justify-between mb-4">
            <View className="flex-1">
              <Text className="text-gray-700">Microphone Enabled</Text>
              <Text className="text-gray-500 text-sm">Start calls with mic on</Text>
            </View>
            <Switch 
              value={micEnabled} 
              onValueChange={setMicEnabled}
              trackColor={{ false: "#374151", true: "#ec4899" }}
              thumbColor={micEnabled ? "#ffffff" : "#9ca3af"}
            />
          </View>

          <View className="flex-row items-center justify-between mb-4">
            <View className="flex-1">
              <Text className="text-gray-700">Camera Enabled</Text>
              <Text className="text-gray-500 text-sm">Start calls with camera on</Text>
            </View>
            <Switch 
              value={cameraEnabled} 
              onValueChange={setCameraEnabled}
              trackColor={{ false: "#374151", true: "#ec4899" }}
              thumbColor={cameraEnabled ? "#ffffff" : "#9ca3af"}
            />
          </View>

          <View className="flex-row items-center justify-between mb-4">
            <View className="flex-1">
              <Text className="text-gray-700">AI Avatar</Text>
              <Text className="text-gray-500 text-sm">Invite AI assistant to calls</Text>
            </View>
            <Switch 
              value={avatarEnabled} 
              onValueChange={setAvatarEnabled}
              trackColor={{ false: "#374151", true: "#ec4899" }}
              thumbColor={avatarEnabled ? "#ffffff" : "#9ca3af"}
            />
          </View>
        </View>

        {/* Notifications */}
        <View className="mb-8">
          <Text className="text-gray-800 text-lg font-semibold mb-4">Notifications</Text>
          
          <View className="flex-row items-center justify-between">
            <View className="flex-1">
              <Text className="text-gray-700">Push Notifications</Text>
              <Text className="text-gray-500 text-sm">Receive call notifications</Text>
            </View>
            <Switch 
              value={notifications} 
              onValueChange={setNotifications}
              trackColor={{ false: "#374151", true: "#ec4899" }}
              thumbColor={notifications ? "#ffffff" : "#9ca3af"}
            />
          </View>
        </View>

        {/* Save Button */}
        <Pressable
          onPress={handleSave}
          disabled={isScraping}
          className={`rounded-2xl px-5 py-4 items-center mb-6 ${isScraping ? 'bg-pink-400' : 'bg-pink-600'}`}
        >
          {isScraping ? (
            <View className="flex-row items-center">
              <ActivityIndicator color="white" size="small" />
              <Text className="text-white text-base font-medium ml-2">Updating Profile...</Text>
            </View>
          ) : (
            <Text className="text-white text-base font-medium">Save Profile</Text>
          )}
        </Pressable>

        {/* Info about social media scraping */}
        {(linkedInUrl.trim() || fullName.trim() || instagramUsername.trim() || twitterUsername.trim()) && (
          <View className="bg-pink-100 rounded-xl p-4 mb-6">
            <View className="flex-row items-start">
              <Ionicons name="information-circle" size={20} color="#db2777" />
              <View className="flex-1 ml-2">
                <Text className="text-pink-900 text-sm font-medium mb-1">Social Media Context</Text>
                <Text className="text-pink-800 text-xs">
                  We'll crawl your LinkedIn profile with advanced web scraping, find your Facebook using your full name, and analyze your Instagram and Twitter accounts to help the AI understand your interests and create better conversation starters for your dates!
                </Text>
              </View>
            </View>
          </View>
        )}

        {/* App Info */}
        <View className="items-center">
          <Text className="text-gray-500 text-sm">AuraDate v1.0.0</Text>
        </View>
      </View>
    </ScrollView>
  );
}
