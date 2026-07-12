package com.teambotics.deskbuddy.mobile.ui.theme

import androidx.compose.ui.graphics.Color

// DeskBuddy brand colors — dashboard aligned
val DeskBuddyAccent = Color(0xFFB45309)          // amber
val DeskBuddyAccentLight = Color(0xFFD97706)
val DeskBuddyAccentDark = Color(0xFF92400E)

// Light mode
val DeskBuddyBackground = Color(0xFFF5F5F7)
val DeskBuddySurface = Color(0xFFFFFFFF)
val DeskBuddySurfaceAlt = Color(0xFFECECEF)
val DeskBuddyText = Color(0xFF18181B)
val DeskBuddyMuted = Color(0xFF6B6B70)
val DeskBuddyBorder = Color(0x14000000)          // rgba(0,0,0,0.08)

// Dark mode
val DeskBuddyBackgroundDark = Color(0xFF111318)    // mockup page bg
val DeskBuddySurfaceDark = Color(0xFF1A1D26)      // mockup card bg
val DeskBuddySurfaceAltDark = Color(0xFF18181B)
val DeskBuddyTextDark = Color(0xFFF2F2F2)        // mockup primary text
val DeskBuddyMutedDark = Color(0xFFA1A1AA)
val DeskBuddySubtleDark = Color(0xFF71717A)
val DeskBuddyBorderDark = Color(0x12FFFFFF)      // rgba(255,255,255,0.07) mockup

// Status colors — dashboard aligned
val DeskBuddyError = Color(0xFFEF4444)           // red
val DeskBuddyBlue = Color(0xFF6366F1)            // thinking indigo

// Legacy aliases for compatibility
val DeskBuddyTextPrimary = DeskBuddyTextDark
val DeskBuddyTextSecondary = DeskBuddyMutedDark
val DeskBuddyTextTertiary = DeskBuddySubtleDark

// Mockup dark theme — from deskbuddy_mobile_ui_redesign.html
val DeskBuddyDividerDark = Color(0xFF2E2E35)      // divider
val DeskBuddyFaintDark = Color(0xFF52525B)        // meta text, event label
val DeskBuddyGreenBright = Color(0xFF16A34A)      // connected dot, working badge
val DeskBuddyGreenBorder = Color(0x4D168060)      // rgba(22,128,60,0.3) connection badge border

// Floating pet bubble colors (android.graphics.Color int values for traditional View usage)
val BUBBLE_BG = 0xFF1E1E2E.toInt()            // card background
val BUBBLE_TEXT = 0xFFE0E0E0.toInt()          // primary text
val BUBBLE_MUTED = 0xFF888888.toInt()         // secondary/muted text
val BUBBLE_BUTTON_BG = 0xFF2A2A3E.toInt()     // button background
val BUBBLE_DIVIDER = 0x33FFFFFF.toInt()       // 20% white divider
