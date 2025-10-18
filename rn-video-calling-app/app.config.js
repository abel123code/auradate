export default {
  expo: {
    name: "AuraDate",
    slug: "auradate",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/images/AuraDate.png",
    scheme: "auradate",
    userInterfaceStyle: "automatic",
    newArchEnabled: false,
    ios: {
      bundleIdentifier: "com.anonymous.auradateapp",
      supportsTablet: true,
      infoPlist: {
        NSCameraUsageDescription: "This app uses the camera for video calls.",
        NSMicrophoneUsageDescription: "This app uses the microphone for calls.",
      },
    },
    android: {
      googleServicesFile: "./google-services.json",
      edgeToEdgeEnabled: true,
      adaptiveIcon: {
        foregroundImage: "./assets/images/AuraDate.png",
        backgroundColor: "#fce7f3",
      },
      permissions: [
        "INTERNET",
        "CAMERA",
        "RECORD_AUDIO",
        "BLUETOOTH",
        "BLUETOOTH_CONNECT",
        "MODIFY_AUDIO_SETTINGS",
      ],
      package: "com.anonymous.auradateapp",
    },
    web: {
      bundler: "metro",
      output: "static",
      favicon: "./assets/images/AuraDate.png",
    },
    plugins: [
      "expo-router",
      [
        "expo-splash-screen",
        {
          image: "./assets/images/AuraDate.png",
          imageWidth: 200,
          resizeMode: "contain",
          backgroundColor: "#fce7f3",
        },
      ],
      [
        "react-native-permissions",
        {
          iosPermissions: ["Camera", "Microphone"],
          androidPermissions: [
            "android.permission.CAMERA",
            "android.permission.RECORD_AUDIO",
            "android.permission.BLUETOOTH_CONNECT",
          ],
        },
      ],
      [
        "expo-notifications",
        {
          icon: "./assets/images/AuraDate.png",
          color: "#ec4899", // Brand pink color for notification tint
          defaultChannel: "default",
          androidMode: "default",
          androidCollapsedTitle: "AuraDate",
        },
      ],
      "@livekit/react-native-expo-plugin",
    ],
    experiments: {
      typedRoutes: true,
    },
    extra: {
      router: {},
      apiUrl: "https://mission-two-server.onrender.com",
      eas: {
        projectId: "09979be6-5cf4-4a38-970a-92d758fde764",
      },
    },
    "owner": "funaiorg",
  },
};
