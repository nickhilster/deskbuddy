package com.teambotics.deskbuddy.mobile.ui.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.teambotics.deskbuddy.mobile.R
import com.teambotics.deskbuddy.mobile.ui.components.DeskBuddyIcons
import com.teambotics.deskbuddy.mobile.ui.theme.*
import com.teambotics.deskbuddy.mobile.util.ConnectionLog

@Composable
internal fun DebugLogSection() {
    val clipboard = LocalClipboardManager.current
    var logText by remember { mutableStateOf(ConnectionLog.dump()) }

    Text(
        stringResource(R.string.settings_debug_log_desc),
        fontSize = 12.sp,
        color = DeskBuddyFaintDark,
        modifier = Modifier.padding(bottom = 12.dp)
    )

    // Refresh button
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        OutlinedButton(
            onClick = { logText = ConnectionLog.dump() },
            border = androidx.compose.foundation.BorderStroke(0.5.dp, DeskBuddyBorderDark),
            shape = RoundedCornerShape(10.dp),
            modifier = Modifier.weight(1f)
        ) {
            Icon(DeskBuddyIcons.Refresh, null, modifier = Modifier.size(14.dp), tint = DeskBuddyMutedDark)
            Spacer(modifier = Modifier.width(4.dp))
            Text(stringResource(R.string.action_refresh), color = DeskBuddyMutedDark, fontSize = 12.sp)
        }
        OutlinedButton(
            onClick = { clipboard.setText(AnnotatedString(logText)) },
            border = androidx.compose.foundation.BorderStroke(0.5.dp, DeskBuddyBorderDark),
            shape = RoundedCornerShape(10.dp),
            modifier = Modifier.weight(1f)
        ) {
            Icon(DeskBuddyIcons.Checks, null, modifier = Modifier.size(14.dp), tint = DeskBuddyMutedDark)
            Spacer(modifier = Modifier.width(4.dp))
            Text(stringResource(R.string.action_copy_all), color = DeskBuddyMutedDark, fontSize = 12.sp)
        }
        OutlinedButton(
            onClick = { ConnectionLog.clear(); logText = "" },
            border = androidx.compose.foundation.BorderStroke(0.5.dp, DeskBuddyBorderDark),
            shape = RoundedCornerShape(10.dp),
            modifier = Modifier.weight(1f)
        ) {
            Text(stringResource(R.string.action_clear), color = DeskBuddyMutedDark, fontSize = 12.sp)
        }
    }

    // Log display
    if (logText.isNotEmpty()) {
        Spacer(modifier = Modifier.height(10.dp))
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(max = 300.dp)
                .background(Color(0xFF111111), RoundedCornerShape(8.dp))
                .border(0.5.dp, DeskBuddyBorderDark, RoundedCornerShape(8.dp))
                .padding(8.dp)
        ) {
            Text(
                logText,
                fontSize = 10.sp,
                color = Color(0xFF88CC88),
                fontFamily = FontFamily.Monospace,
                lineHeight = 14.sp,
                modifier = Modifier.verticalScroll(rememberScrollState())
            )
        }
    } else {
        Spacer(modifier = Modifier.height(8.dp))
        Text(stringResource(R.string.settings_no_log), fontSize = 12.sp, color = DeskBuddyFaintDark)
    }
}
