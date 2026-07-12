package com.teambotics.deskbuddy.mobile.ui.theme

import android.app.Activity
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private fun findActivity(context: android.content.Context): Activity? {
    var ctx = context
    while (ctx is android.content.ContextWrapper) {
        if (ctx is Activity) return ctx
        ctx = ctx.baseContext
    }
    return null
}

private val DarkColorScheme = darkColorScheme(
    primary = DeskBuddyAccent,
    onPrimary = Color.White,
    primaryContainer = DeskBuddyAccentDark,
    onPrimaryContainer = Color.White,
    secondary = DeskBuddyAccentLight,
    onSecondary = Color.White,
    background = DeskBuddyBackgroundDark,
    onBackground = DeskBuddyTextDark,
    surface = DeskBuddySurfaceDark,
    onSurface = DeskBuddyTextDark,
    surfaceVariant = DeskBuddySurfaceAltDark,
    onSurfaceVariant = DeskBuddyMutedDark,
    error = DeskBuddyError,
    onError = Color.White,
    outline = DeskBuddyBorderDark,
    outlineVariant = Color(0xFF333340),
)

private val LightColorScheme = lightColorScheme(
    primary = DeskBuddyAccent,
    onPrimary = Color.White,
    primaryContainer = DeskBuddyAccentLight,
    onPrimaryContainer = DeskBuddyAccentDark,
    secondary = DeskBuddyAccentDark,
    onSecondary = Color.White,
    background = DeskBuddyBackground,
    onBackground = DeskBuddyText,
    surface = DeskBuddySurface,
    onSurface = DeskBuddyText,
    surfaceVariant = DeskBuddySurfaceAlt,
    onSurfaceVariant = DeskBuddyMuted,
    error = DeskBuddyError,
    onError = Color.White,
    outline = DeskBuddyBorder,
    outlineVariant = Color(0xFFE0E0E0),
)

@Composable
fun DeskBuddyMobileTheme(
    content: @Composable () -> Unit
) {
    val view = LocalView.current
    val isDark = androidx.compose.foundation.isSystemInDarkTheme()
    val colorScheme = if (isDark) DarkColorScheme else LightColorScheme

    if (!view.isInEditMode) {
        SideEffect {
            val window = findActivity(view.context)?.window ?: return@SideEffect
            window.statusBarColor = colorScheme.background.toArgb()
            window.navigationBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !isDark
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = DeskBuddyTypography,
        content = content
    )
}
