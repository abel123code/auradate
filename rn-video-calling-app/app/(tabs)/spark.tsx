import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { API_BASE_URL } from '../../config/api';

interface User {
  id: string;
  display_name: string;
}

export default function SparkScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<User[]>([]);
  const [searching, setSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      Alert.alert('Error', 'Please enter a username to search');
      return;
    }

    setSearching(true);
    setHasSearched(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/users`);
      const data = await response.json();
      
      // Filter users by search query (case-insensitive partial match)
      const filteredUsers = data.users.filter((user: User) => 
        user.display_name.toLowerCase().includes(searchQuery.toLowerCase())
      );
      
      setSearchResults(filteredUsers);
    } catch (error) {
      console.error('Error searching users:', error);
      Alert.alert('Error', 'Failed to search users');
    } finally {
      setSearching(false);
    }
  };

  const handleUserSelect = (user: User) => {
    router.push({
      pathname: '/memories',
      params: { username: user.display_name }
    });
  };

  return (
    <View className="flex-1 bg-pink-50">
      <View className="p-6">
        <View className="mb-8">
          <Text className="text-3xl font-bold text-gray-800 mb-2">
            Connection, simplified
          </Text>
          <Text className="text-gray-600">
            Where good talks become good dates
          </Text>
        </View>

        <View className="bg-white p-6 rounded-2xl mb-4">
          <View className="flex-row items-center bg-gray-50 rounded-full px-4 py-3 mb-4 border border-gray-200">
            <Ionicons name="search" size={20} color="#9CA3AF" />
            <TextInput
              value={searchQuery}
              onChangeText={setSearchQuery}
              placeholder="Enter username..."
              className="flex-1 ml-3 text-gray-800"
              placeholderTextColor="#9CA3AF"
            />
          </View>
          
          <TouchableOpacity
            onPress={handleSearch}
            disabled={searching || !searchQuery.trim()}
            className={`rounded-full py-4 ${
              searching || !searchQuery.trim() 
                ? 'bg-gray-300' 
                : 'bg-pink-600'
            }`}
          >
            {searching ? (
              <View className="flex-row items-center justify-center">
                <ActivityIndicator size="small" color="white" />
                <Text className="text-white font-semibold ml-2">Searching...</Text>
              </View>
            ) : (
              <Text className="text-white font-semibold text-center text-base">Search</Text>
            )}
          </TouchableOpacity>
        </View>

        {searchResults.length > 0 && (
          <View className="bg-white rounded-2xl overflow-hidden">
            <View className="px-6 py-4 bg-pink-50">
              <Text className="text-gray-800 font-semibold text-base">
                {searchResults.length} {searchResults.length === 1 ? 'user' : 'users'} found
              </Text>
            </View>
            <ScrollView className="max-h-80">
              {searchResults.map((user, index) => (
                <TouchableOpacity
                  key={user.id}
                  onPress={() => handleUserSelect(user)}
                  className={`px-6 py-4 flex-row items-center ${
                    index !== searchResults.length - 1 ? 'border-b border-gray-100' : ''
                  }`}
                  activeOpacity={0.7}
                >
                  <View className="bg-pink-600 w-12 h-12 rounded-full items-center justify-center mr-4">
                    <Ionicons name="person" size={24} color="white" />
                  </View>
                  <View className="flex-1">
                    <Text className="text-gray-800 font-semibold text-base mb-1">
                      {user.display_name}
                    </Text>
                    <Text className="text-gray-500 text-sm">
                      Tap to view profile
                    </Text>
                  </View>
                  <Ionicons name="chevron-forward" size={24} color="#d1d5db" />
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        )}

        {hasSearched && searchResults.length === 0 && !searching && (
          <View className="bg-white p-8 rounded-2xl items-center">
            <View className="bg-gray-100 w-16 h-16 rounded-full items-center justify-center mb-4">
              <Ionicons name="search-outline" size={32} color="#9ca3af" />
            </View>
            <Text className="text-gray-800 font-semibold text-lg mb-2">
              No users found
            </Text>
            <Text className="text-gray-500 text-center">
              Try a different username
            </Text>
          </View>
        )}
      </View>
    </View>
  );
}