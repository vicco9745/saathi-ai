package in.saathi.app;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Person;
import android.app.Service;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.PixelFormat;
import android.graphics.Shader;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.Icon;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.os.PowerManager;
import android.os.SystemClock;
import android.provider.Settings;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.widget.Chronometer;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class CallService extends Service {
    static CallService inst;
    private PowerManager.WakeLock wl;
    private boolean muted = false;
    private long startElapsed = 0;
    private View pill;
    private ImageView micBtn;
    private WindowManager wm;
    private final Handler ui = new Handler(Looper.getMainLooper());

    @Override
    public IBinder onBind(Intent i) { return null; }

    private int dp(int v) { return (int) (v * getResources().getDisplayMetrics().density); }

    private void js(final String code) {
        ui.post(() -> {
            try {
                if (MainActivity.web != null) MainActivity.web.evaluateJavascript(code, null);
            } catch (Exception e) { }
        });
    }

    private Icon avatar() {
        int s = 192;
        Bitmap bm = Bitmap.createBitmap(s, s, Bitmap.Config.ARGB_8888);
        Canvas c = new Canvas(bm);
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        p.setShader(new LinearGradient(0, 0, 0, s, 0xFF3B7BF2, 0xFFD6E6FF, Shader.TileMode.CLAMP));
        c.drawCircle(s / 2f, s / 2f, s / 2f, p);
        return Icon.createWithBitmap(bm);
    }

    private Notification build() {
        String ch = "saathi_call";
        int fl = PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT;
        Intent open = new Intent(this, MainActivity.class);
        open.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent po = PendingIntent.getActivity(this, 0, open, fl);
        Intent end = new Intent(this, CallService.class);
        end.setAction("END");
        PendingIntent pe = PendingIntent.getService(this, 1, end, fl);
        Intent mu = new Intent(this, CallService.class);
        mu.setAction("MUTE");
        PendingIntent pm = PendingIntent.getService(this, 2, mu, fl);
        Notification.Builder nb = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, ch) : new Notification.Builder(this);
        nb.setSmallIcon(android.R.drawable.ic_btn_speak_now)
          .setContentIntent(po)
          .setOngoing(true);
        if (Build.VERSION.SDK_INT >= 31) {
            Person who = new Person.Builder().setName("Saathi Voice").setIcon(avatar()).setImportant(true).build();
            nb.setStyle(Notification.CallStyle.forOngoingCall(who, pe));
            nb.setCategory(Notification.CATEGORY_CALL);
            nb.addAction(new Notification.Action.Builder(Icon.createWithResource(this, android.R.drawable.ic_lock_silent_mode), muted ? "UNMUTE" : "MUTE", pm).build());
        } else {
            nb.setContentTitle("Saathi Voice");
            nb.addAction(android.R.drawable.ic_lock_silent_mode, muted ? "UNMUTE" : "MUTE", pm);
            nb.addAction(android.R.drawable.ic_menu_close_clear_cancel, "HANG UP", pe);
        }
        return nb.build();
    }

    private void refreshPill() {
        if (micBtn != null) {
            micBtn.setColorFilter(muted ? 0xFFD93025 : 0xFF1B1B1F);
            micBtn.setImageResource(muted ? android.R.drawable.ic_lock_silent_mode : android.R.drawable.ic_btn_speak_now);
        }
    }

    private void toggleMute() {
        muted = !muted;
        js("try{callMuted=" + muted + ";renderCallMicIcon();}catch(e){}");
        NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        nm.notify(1, build());
        ui.post(this::refreshPill);
    }

    private void endCall() {
        js("try{stopCall()}catch(e){}");
        stopSelf();
    }

    void showPill() {
        ui.post(() -> {
            try {
                if (pill != null) return;
                if (Build.VERSION.SDK_INT >= 23 && !Settings.canDrawOverlays(this)) return;
                wm = (WindowManager) getSystemService(WINDOW_SERVICE);
                LinearLayout root = new LinearLayout(this);
                root.setOrientation(LinearLayout.HORIZONTAL);
                root.setGravity(Gravity.CENTER_VERTICAL);
                root.setPadding(dp(14), dp(12), dp(14), dp(12));
                GradientDrawable bg = new GradientDrawable();
                bg.setColor(0xFFF6F7FB);
                bg.setCornerRadius(dp(40));
                root.setBackground(bg);

                ImageView av = new ImageView(this);
                GradientDrawable ring = new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{0xFF3B7BF2, 0xFFA9C7FF});
                ring.setShape(GradientDrawable.OVAL);
                av.setBackground(ring);
                av.setImageResource(android.R.drawable.ic_btn_speak_now);
                av.setColorFilter(0xFFFFFFFF);
                av.setPadding(dp(11), dp(11), dp(11), dp(11));
                root.addView(av, new LinearLayout.LayoutParams(dp(48), dp(48)));

                LinearLayout col = new LinearLayout(this);
                col.setOrientation(LinearLayout.VERTICAL);
                TextView t1 = new TextView(this);
                t1.setText("Live");
                t1.setTextSize(20);
                t1.setTypeface(null, Typeface.BOLD);
                t1.setTextColor(0xFF1B1B1F);
                Chronometer ch = new Chronometer(this);
                ch.setTextSize(16);
                ch.setTextColor(0xFF6B6F76);
                ch.setBase(startElapsed);
                ch.start();
                col.addView(t1);
                col.addView(ch);
                LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f);
                cp.leftMargin = dp(14);
                root.addView(col, cp);

                micBtn = new ImageView(this);
                micBtn.setPadding(dp(12), dp(12), dp(12), dp(12));
                micBtn.setOnClickListener(v -> toggleMute());
                root.addView(micBtn, new LinearLayout.LayoutParams(dp(50), dp(50)));
                refreshPill();

                ImageView x = new ImageView(this);
                x.setImageResource(android.R.drawable.ic_menu_close_clear_cancel);
                x.setColorFilter(0xFF1B1B1F);
                x.setPadding(dp(12), dp(12), dp(12), dp(12));
                x.setOnClickListener(v -> endCall());
                root.addView(x, new LinearLayout.LayoutParams(dp(50), dp(50)));

                int w = getResources().getDisplayMetrics().widthPixels - dp(48);
                WindowManager.LayoutParams lp = new WindowManager.LayoutParams(w, WindowManager.LayoutParams.WRAP_CONTENT,
                    Build.VERSION.SDK_INT >= 26 ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY : WindowManager.LayoutParams.TYPE_PHONE,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
                    PixelFormat.TRANSLUCENT);
                lp.gravity = Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL;
                lp.y = dp(96);
                wm.addView(root, lp);
                pill = root;
            } catch (Exception e) {
                pill = null;
                micBtn = null;
            }
        });
    }

    void hidePill() {
        ui.post(() -> {
            try {
                if (pill != null && wm != null) wm.removeView(pill);
            } catch (Exception e) { }
            pill = null;
            micBtn = null;
        });
    }

    @Override
    public int onStartCommand(Intent i, int flags, int id) {
        String a = i != null ? i.getAction() : null;
        NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if ("END".equals(a)) {
            endCall();
            return START_NOT_STICKY;
        }
        if ("MUTE".equals(a)) {
            toggleMute();
            return START_NOT_STICKY;
        }
        inst = this;
        muted = false;
        startElapsed = SystemClock.elapsedRealtime();
        if (Build.VERSION.SDK_INT >= 26) {
            nm.createNotificationChannel(new NotificationChannel("saathi_call", "Saathi call", NotificationManager.IMPORTANCE_LOW));
        }
        if (Build.VERSION.SDK_INT >= 29) {
            startForeground(1, build(), ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE);
        } else {
            startForeground(1, build());
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
        try { if (pill != null && wm != null) wm.removeView(pill); } catch (Exception e) { }
        pill = null;
        micBtn = null;
        inst = null;
        try { if (wl != null && wl.isHeld()) wl.release(); } catch (Exception e) { }
        wl = null;
        super.onDestroy();
    }
}
