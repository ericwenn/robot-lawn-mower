package com.example.jesper.myapplication;

import android.app.Dialog;
import android.content.DialogInterface;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.*;



public class MainActivity extends AppCompatActivity{
    public static String ip_address;
    public static String port;

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        View view = LayoutInflater.from(this).inflate(R.layout.user_input, null);


        //Ask for ip and port
        AlertDialog.Builder alertBuilder = new AlertDialog.Builder(this);
        alertBuilder.setView(view);
        final EditText ip = (EditText) view.findViewById(R.id.ip_address);
        final EditText prt = (EditText) view.findViewById(R.id.port);
        alertBuilder.setCancelable(true)
                .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        MainActivity.ip_address = ip.getText().toString();
                        MainActivity.port = prt.getText().toString();
                    }
                });

        Dialog dialog = alertBuilder.create();
        dialog.show();

        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
        fragmentTransaction.replace(R.id.frameLayout, new MapFragment());
        fragmentTransaction.commit();

        InputMonitor im = new InputMonitor(this);
    }

}
