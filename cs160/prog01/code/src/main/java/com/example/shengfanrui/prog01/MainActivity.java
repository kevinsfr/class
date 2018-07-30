package com.example.shengfanrui.prog01;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    private EditText input;
    private TextView output, equivalent, unit, unit2;
    private RadioGroup type, type2;
    private RadioButton pushUp, sitUp, sqauts, leg_lift, plank, jumping_jacks, pullUp, cycling, walking, jogging, swimming, stair_climbing;
    private RadioButton pushUp2, sitUp2, sqauts2, leg_lift2, plank2, jumping_jacks2, pullUp2, cycling2, walking2, jogging2, swimming2, stair_climbing2;
    private Button btn;
    private int x1, x2, number;
    private double calories;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        input = (EditText) findViewById(R.id.number);
        output = (TextView) findViewById((R.id.output));
        equivalent = (TextView) findViewById(R.id.otherType);
        unit = (TextView) findViewById(R.id.unit);
        unit2 = (TextView) findViewById(R.id.unit2);
        type = (RadioGroup) findViewById(R.id.type);
        type2 = (RadioGroup) findViewById(R.id.type2);
        btn = (Button) findViewById(R.id.convert);
        type.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                switch (checkedId) {
                    case R.id.pushup: x1 = 350;
                        unit.setText("Reps");
                        break;
                    case R.id.situp: x1 = 200;
                        unit.setText("Reps");
                        break;
                    case R.id.squats: x1 = 225;
                        unit.setText("Reps");
                        break;
                    case R.id.leg_lift: x1 = 25;
                        unit.setText("Minutes");
                        break;
                    case R.id.plank: x1 = 25;
                        unit.setText("Minutes");
                        break;
                    case R.id.jumping_jacks: x1 = 10;
                        unit.setText("Minutes");
                        break;
                    case R.id.pullup: x1 = 100;
                        unit.setText("Reps");
                        break;
                    case R.id.cycling: x1 = 12;
                        unit.setText("Minutes");
                        break;
                    case R.id.walking: x1 = 20;
                        unit.setText("Minutes");
                        break;
                    case R.id.jogging: x1 = 12;
                        unit.setText("Minutes");
                        break;
                    case R.id.swimming: x1 = 13;
                        unit.setText("Minutes");
                        break;
                    default: x1 = 15;
                        unit.setText("Minutes");
                        break;
                }
            }
        });
        type2.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                switch (checkedId) {
                    case R.id.pushup2: x2 = 350;
                        unit2.setText("Reps");
                        break;
                    case R.id.situp2: x2 = 200;
                        unit2.setText("Reps");
                        break;
                    case R.id.squats2: x2 = 225;
                        unit2.setText("Reps");
                        break;
                    case R.id.leg_lift2: x2 = 25;
                        unit2.setText("Minutes");
                        break;
                    case R.id.plank2: x2 = 25;
                        unit2.setText("Minutes");
                        break;
                    case R.id.jumping_jacks2: x2 = 10;
                        unit2.setText("Minutes");
                        break;
                    case R.id.pullup2: x2 = 100;
                        unit2.setText("Reps");
                        break;
                    case R.id.cycling2: x2 = 12;
                        unit2.setText("Minutes");
                        break;
                    case R.id.walking2: x2 = 20;
                        unit2.setText("Minutes");
                        break;
                    case R.id.jogging2: x2 = 12;
                        unit2.setText("Minutes");
                        break;
                    case R.id.swimming2: x2 = 13;
                        unit2.setText("Minutes");
                        break;
                    default: x2 = 15;
                        unit2.setText("Minutes");
                        break;
                }
                double amount = x2 * calories / 100;
                int y = (int) Math.round(amount);
                equivalent.setText(String.valueOf(y));
            }
        });
        btn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                number = Integer.parseInt(input.getText().toString());
                calories = (double) number / x1 * 100;
                calories = (double) Math.round(calories * 100) / 100;
                output.setText(String.valueOf(calories) + " Cal");
            }
        });

    }

}
