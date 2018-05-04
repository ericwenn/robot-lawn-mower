package com.example.jesper.myapplication;

import android.widget.Button;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ToggleButton;
import com.android.volley.*;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;



public class InputMonitor implements View.OnClickListener {
    private MainActivity main;
    Button left;
    Button right;
    Button up;
    Button down;
    ImageButton stop;
    Button probe;
    ToggleButton tb;
    RequestQueue requestQueue;
    String adr;
    StringRequest sReq;

    public InputMonitor(MainActivity main){
        this.main = main;

        left = (Button) main.findViewById(R.id.button);
        right = (Button) main.findViewById(R.id.button2);
        up = (Button) main.findViewById(R.id.button3);
        down = (Button) main.findViewById(R.id.button4);
        stop = (ImageButton) main.findViewById(R.id.button5);
        probe = (Button) main.findViewById(R.id.button6);
        tb = (ToggleButton) main.findViewById((R.id.toggleButton));

        left.setOnClickListener(this);
        right.setOnClickListener(this);
        up.setOnClickListener(this);
        down.setOnClickListener(this);
        stop.setOnClickListener(this);
        tb.setOnClickListener(this);

        probe.setOnClickListener(this);
        probe.setClickable(false);
        probe.setAlpha(0.5f);

        requestQueue = Volley.newRequestQueue(main);

    }

    @Override
    public void onClick(View v){
        try {
            adr = "http://"+MainActivity.ip_address+":"+MainActivity.port;
            if (v.getId() == left.getId()) {
                sReq = new StringRequest(Request.Method.POST, adr+"/config/left",

                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                       //Something on error
                    }
                });
                requestQueue.add(sReq);

            } else if (v.getId() == right.getId()) {
                sReq = new StringRequest(Request.Method.POST, adr+"/config/right",

                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //Something on error
                    }
                });
                requestQueue.add(sReq);

            } else if (v.getId() == up.getId()) {
                sReq = new StringRequest(Request.Method.POST, adr+"/config/forward",

                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //Something on error
                    }
                });
                requestQueue.add(sReq);

            } else if (v.getId() == down.getId()) {
                sReq = new StringRequest(Request.Method.POST, adr+"/config/backward",

                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //Something on error
                    }
                });
                requestQueue.add(sReq);

            } else if (v.getId() == stop.getId()) {
                sReq = new StringRequest(Request.Method.POST, adr+"/config/stop",

                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //Something on error
                    }
                });
                requestQueue.add(sReq);

            } else if (v.getId() == tb.getId()){
                if(tb.isChecked()){
                    probe.setClickable(true);
                    probe.setAlpha(1.0f);
                    sReq = new StringRequest(Request.Method.POST, adr+"/config/on",

                            new Response.Listener<String>() {
                                @Override
                                public void onResponse(String response) {
                                    // Display the first 500 characters of the response string.
                                }
                            }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            //Something on error
                        }
                    });
                    requestQueue.add(sReq);
                }else{
                    probe.setClickable(false);
                    probe.setAlpha(0.5f);
                    sReq = new StringRequest(Request.Method.POST, adr+"/config/off",

                            new Response.Listener<String>() {
                                @Override
                                public void onResponse(String response) {
                                    // Display the first 500 characters of the response string.
                                }
                            }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            //Something on error
                        }
                    });
                    requestQueue.add(sReq);
                }
            } else if (v.getId() == probe.getId()){
                sReq = new StringRequest(Request.Method.POST, adr+"/config/probe",

                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //Something on error
                    }
                });
                requestQueue.add(sReq);
            }
        }catch(Exception e){
            e.getMessage();
        }
    }

}
