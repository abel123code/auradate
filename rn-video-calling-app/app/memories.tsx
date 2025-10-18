import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, router } from 'expo-router';
import { API_BASE_URL } from '../config/api';
import { useDisplayName } from '../hooks/useDisplayName';

interface Memory {
  memory: string;
  timestamp?: string;
  metadata?: {
    timestamp?: string;
    role?: string;
  };
}

interface UserMemoriesResponse {
  username: string;
  memories: Memory[];
  count: number;
}

export default function MemoriesScreen() {
  const { username } = useLocalSearchParams<{ username: string }>();
  const { displayName } = useDisplayName();
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (username) {
      fetchUserMemories();
    }
  }, [username]);

  const fetchUserMemories = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE_URL}/api/user-memories/${encodeURIComponent(username)}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          setError('User not found');
        } else {
          setError('Failed to load memories');
        }
        return;
      }

      const data: UserMemoriesResponse = await response.json();
      setMemories(data.memories || []);
    } catch (error) {
      console.error('Error fetching user memories:', error);
      setError('Failed to load memories');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    router.back();
  };

  const handleStartConversation = () => {
    if (!displayName) {
      Alert.alert('Error', 'Please set your display name in profile first');
      return;
    }
    
    router.push({
      pathname: '/voice-facilitator',
      params: { 
        otherUser: username,
        currentUser: displayName 
      }
    });
  };

  if (loading) {
    return (
      <View className="flex-1 bg-pink-50 items-center justify-center">
        <ActivityIndicator size="large" color="#ec4899" />
        <Text className="text-gray-600 mt-4">Loading memories...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 bg-pink-50">
        <View className="p-4 bg-white border-b border-pink-200">
          <TouchableOpacity onPress={handleBack} className="flex-row items-center">
            <Ionicons name="arrow-back" size={24} color="#ec4899" />
            <Text className="text-gray-800 ml-2 text-lg font-semibold">Back</Text>
          </TouchableOpacity>
        </View>

        <View className="flex-1 items-center justify-center p-8">
          <Ionicons name="alert-circle-outline" size={64} color="#ef4444" />
          <Text className="text-gray-800 text-xl font-semibold mt-6 text-center">
            {error}
          </Text>
          <Text className="text-gray-600 text-center mt-2">
            {error === 'User not found' 
              ? `No user found with username "${username}"`
              : 'Please try again later'
            }
          </Text>
          <TouchableOpacity
            onPress={handleBack}
            className="mt-8 bg-pink-600 px-8 py-3 rounded-full"
          >
            <Text className="text-white font-semibold">Back to Search</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-pink-50">

      {/* Content */}
      {memories.length === 0 ? (
        <View className="flex-1 items-center justify-center p-8">
          <Ionicons name="time-outline" size={64} color="#9ca3af" />
          <Text className="text-gray-600 text-center mt-6 text-lg font-medium">
            No memories yet
          </Text>
          <Text className="text-gray-500 text-center mt-2">
            This user hasn't had any conversations
          </Text>
        </View>
      ) : (
        <View className="flex-1 items-center justify-center p-8">
          <View className="bg-white p-8 rounded-2xl border border-pink-200 w-full max-w-sm">
            <View className="items-center mb-6">
              <View className="bg-pink-100 w-16 h-16 rounded-full items-center justify-center mb-4">
                <Ionicons name="chatbubbles" size={32} color="#ec4899" />
              </View>
              <Text className="text-gray-700 text-center text-base">
                Ready to start a conversation with {username}
              </Text>
            </View>
            
            <TouchableOpacity
              onPress={handleStartConversation}
              className="bg-pink-600 py-4 rounded-full flex-row items-center justify-center"
            >
              <Ionicons name="chatbubbles" size={20} color="white" />
              <Text className="text-white font-semibold text-lg ml-2">
                Start Conversation
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </View>
  );
}