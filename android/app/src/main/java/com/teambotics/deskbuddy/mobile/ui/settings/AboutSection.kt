package com.teambotics.deskbuddy.mobile.ui.settings

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.teambotics.deskbuddy.mobile.R
import com.teambotics.deskbuddy.mobile.ui.components.DeskBuddyIcons
import com.teambotics.deskbuddy.mobile.ui.theme.*

@Composable
internal fun AboutSection() {
    val clipboard = LocalClipboardManager.current
    val context = LocalContext.current

    Text(
        stringResource(R.string.about_subtitle),
        fontSize = 14.sp,
        fontWeight = FontWeight.Medium,
        color = DeskBuddyTextDark,
        modifier = Modifier.padding(bottom = 4.dp)
    )
    Text(
        "A mobile companion for your AI coding journey.",
        fontSize = 12.sp,
        color = DeskBuddyFaintDark,
        modifier = Modifier.padding(bottom = 12.dp)
    )

    val versionName = try {
        com.teambotics.deskbuddy.mobile.BuildConfig.VERSION_NAME
    } catch (e: Exception) {
        android.util.Log.w("Settings", "BuildConfig access failed", e)
        "?"
    }
    AboutRow(stringResource(R.string.about_version), "v$versionName", DeskBuddyIcons.Activity)
    AboutRow(stringResource(R.string.about_repo), "https://github.com/nickhilster/deskbuddy", DeskBuddyIcons.Folder)
    AboutRow(stringResource(R.string.about_fork), "https://github.com/rullerzhou-afk/clawd-on-desk", DeskBuddyIcons.Folder)
    AboutRow(stringResource(R.string.about_license), "AGPL-3.0 · © 2026 Ruller_Lulu", DeskBuddyIcons.Shield)
    AboutRow(stringResource(R.string.about_author), stringResource(R.string.about_author_name), DeskBuddyIcons.Robot)
    AboutRow(stringResource(R.string.about_maintainer), "@rullerzhou-afk, @nickhilster, @YOIMIYA66", DeskBuddyIcons.Pencil)
    AboutRow(stringResource(R.string.about_mobile_maintainer), "@Bynlk", DeskBuddyIcons.Pencil)

    Spacer(modifier = Modifier.height(12.dp))
    OutlinedButton(
        onClick = {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://github.com/nickhilster/deskbuddy/releases/latest"))
            context.startActivity(intent)
        },
        border = androidx.compose.foundation.BorderStroke(0.5.dp, DeskBuddyBorderDark),
        shape = RoundedCornerShape(10.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Icon(DeskBuddyIcons.Refresh, null, modifier = Modifier.size(16.dp), tint = DeskBuddyMutedDark)
        Spacer(modifier = Modifier.width(6.dp))
        Text(stringResource(R.string.about_check_update), color = DeskBuddyMutedDark)
    }
}

@Composable
private fun AboutRow(label: String, value: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    val clipboard = LocalClipboardManager.current
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { clipboard.setText(AnnotatedString(value)) }
            .padding(vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, null, tint = DeskBuddyFaintDark, modifier = Modifier.size(14.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text(label, fontSize = 12.sp, color = DeskBuddyFaintDark, modifier = Modifier.width(80.dp))
        Text(value, fontSize = 12.sp, color = DeskBuddyTextDark, fontFamily = FontFamily.Monospace, modifier = Modifier.weight(1f))
        Icon(DeskBuddyIcons.Checks, null, tint = DeskBuddyFaintDark.copy(alpha = 0.5f), modifier = Modifier.size(12.dp))
    }
}
