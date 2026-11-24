package in.saathi.app;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.os.PowerManager;

public class CallService extends Service {
    private PowerManager.WakeLock wl;

    @Override
    public IBinder onBind(Intent i) { return null; }

    @Override
    public int onStartCommand(Intent i, int flags, int id) {
        if (i != null && "END".equals(i.getAction())) {
            new Handler(Looper.getMainLooper()).post(() -> {
                try {
                    if (MainActivity.web != null) MainActivity.web.evaluateJavascript("try{stopCall()}catch(e){}", null);
                } catch (Exception e) { }
            });
            stopSelf();
            return START_NOT_STICKY;
        }
        String ch = "saathi_call";
        NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26) {
            nm.createNotificationChannel(new NotificationChannel(ch, "Saathi call", NotificationManager.IMPORTANCE_LOW));
        }
        int fl = PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT;
        Intent open = new Intent(this, MainActivity.class);
        open.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent po = PendingIntent.getActivity(this, 0, open, fl);
        Intent end = new Intent(this, CallService.class);
        end.setAction("END");
        PendingIntent pe = PendingIntent.getService(this, 1, end, fl);
        Notification.Builder nb = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, ch) : new Notification.Builder(this);
        nb.setSmallIcon(android.R.drawable.ic_btn_speak_now)
          .setContentTitle("Saathi call chal rahi hai")
          .setContentText("Kaatne ke liye neeche button dabao")
          .setContentIntent(po)
          .setOngoing(true)
          .setUsesChronometer(true)
          .setWhen(System.currentTimeMillis())
          .addAction(android.R.drawable.ic_menu_close_clear_cancel, "Call kaato", pe);
        if (Build.VERSION.SDK_INT >= 29) {
            startForeground(1, nb.build(), ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE);
        } else {
            startForeground(1, nb.build());
        }
        if (wl == null) {
            PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
            wl = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "saathi:call");
            wl.acquire(4 * 60 * 60 * 1000L);
        }
        return START_NOT_STICKY;
    }

    @Override
    public void onDestroy() {
        try { if (wl != null && wl.isHeld()) wl.release(); } catch (Exception e) { }
        wl = null;
        super.onDestroy();
    }
}
