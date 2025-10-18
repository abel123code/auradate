import { router } from "expo-router";
import { useState } from "react";
import { Pressable, Text, View, Image, ScrollView } from "react-native";
import { Ionicons } from '@expo/vector-icons';
import { useDisplayName } from '@/hooks/useDisplayName';

// Function to generate a unique room name
const generateRoomName = () => {
  const timestamp = Date.now().toString(36);
  const randomStr = Math.random().toString(36).substring(2, 8);
  return `room-${timestamp}-${randomStr}`;
};

export default function DateScreen() {
  const { displayName, isLoading } = useDisplayName();
  const [selectedAvatar, setSelectedAvatar] = useState<'alex' | 'emma' | null>(null);

  const canJoin = displayName && displayName.trim().length > 0 && selectedAvatar;

  const handleJoin = async () => {
    const roomName = generateRoomName();
    
    // For FE-only phase, just navigate with params.
    router.push({
      pathname: "/call",
      params: { 
        room: roomName, 
        name: displayName, 
        avatarName: selectedAvatar,
        mic: "true", 
        cam: "true"
      },
    });
  };

  return (
    <ScrollView className="flex-1 bg-pink-50" contentContainerStyle={{ flexGrow: 1 }}>
      <View className="flex-1 items-center justify-center px-5 py-8">
        {/* Header */}
        <View className="items-center mb-8">
          <Text className="text-gray-800 text-3xl font-bold mb-2">
            Choose Your Date 💕
          </Text>
          <Text className="text-gray-600 text-lg text-center">
            Select an AI companion to chat with
          </Text>
        </View>

        {/* Avatar Selection */}
        <View className="w-full gap-4 mb-8">
          {/* Male Avatar Card */}
          <Pressable
            onPress={() => setSelectedAvatar('alex')}
            className={`bg-white rounded-2xl p-6 border-2 shadow-sm ${
              selectedAvatar === 'alex'
                ? 'border-pink-500 bg-pink-50'
                : 'border-pink-200'
            }`}
          >
            <View className="flex-row items-center space-x-5">
              <View className="w-16 h-16 rounded-full overflow-hidden flex-shrink-0">
                <Image 
                  source={require('../../assets/images/hudson.png')}
                  className="w-full h-full"
                  resizeMode="cover"
                />
              </View>
              <View className="flex-1 ml-2">
                <Text className="text-gray-800 text-xl font-semibold">Alex</Text>
                <Text className="text-gray-600 text-sm">Flirty quips, real chemistry</Text>
                <Text className="text-gray-500 text-xs mt-1">AI Dating Companion</Text>
              </View>
              {selectedAvatar === 'alex' && (
                <Ionicons name="checkmark-circle" size={24} color="#ec4899" />
              )}
            </View>
          </Pressable>

          {/* Female Avatar Card */}
          <Pressable
            onPress={() => setSelectedAvatar('emma')}
            className={`bg-white rounded-2xl p-6 border-2 shadow-sm ${
              selectedAvatar === 'emma'
                ? 'border-pink-500 bg-pink-50'
                : 'border-pink-200'
            }`}
          >
            <View className="flex-row items-center space-x-5">
              <View className="w-16 h-16 rounded-full overflow-hidden flex-shrink-0">
                <Image 
                  source={require('../../assets/images/sara.png')}
                  className="w-full h-full"
                  resizeMode="cover"
                />
              </View>
              <View className="flex-1 ml-2">
                <Text className="text-gray-800 text-xl font-semibold">Emma</Text>
                <Text className="text-gray-600 text-sm">Gentle warmth, thoughtful chat</Text>
                <Text className="text-gray-500 text-xs mt-1">AI Dating Companion</Text>
              </View>
              {selectedAvatar === 'emma' && (
                <Ionicons name="checkmark-circle" size={24} color="#ec4899" />
              )}
            </View>
          </Pressable>
        </View>

        {/* Start Date Button */}
        <Pressable
          onPress={handleJoin}
          disabled={!canJoin}
          className={`w-full rounded-2xl px-8 py-5 items-center shadow-lg ${
            canJoin 
              ? "bg-pink-600" 
              : "bg-gray-400"
          }`}
        >
          <Text className="text-white text-lg font-semibold">
            {canJoin ? "💕 Start Your Date" : "Select an avatar to continue"}
          </Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
