package in.saathi.app;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    static WebView web;
    private boolean asked = false;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        if (Build.VERSION.SDK_INT >= 33) {
            requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO, Manifest.permission.POST_NOTIFICATIONS}, 1);
        } else if (Build.VERSION.SDK_INT >= 23) {
            requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, 1);
        }
        web = new WebView(this);
        setContentView(web);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        web.setWebViewClient(new WebViewClient());
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest r) {
                runOnUiThread(() -> r.grant(r.getResources()));
            }
        });
        web.addJavascriptInterface(new Object() {
            @JavascriptInterface
            public void start() {
                Intent i = new Intent(MainActivity.this, CallService.class);
                i.setAction("START");
                if (Build.VERSION.SDK_INT >= 26) startForegroundService(i); else startService(i);
                runOnUiThread(() -> {
                    if (Build.VERSION.SDK_INT >= 23 && !asked && !Settings.canDrawOverlays(MainActivity.this)) {
                        asked = true;
                        startActivity(new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:" + getPackageName())));
                    }
                });
            }
            @JavascriptInterface
            public void stop() {
                stopService(new Intent(MainActivity.this, CallService.class));
            }
        }, "SaathiNative");
        web.loadUrl("https://vicco9745.github.io/saathi-ai/?app=1");
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (CallService.inst != null) CallService.inst.showPill();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (CallService.inst != null) CallService.inst.hidePill();
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) web.goBack(); else moveTaskToBack(true);
    }
}
