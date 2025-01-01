import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const data = [
  { name: 'Jan', value: 400 },
  { name: 'Feb', value: 300 },
  { name: 'Mar', value: 600 },
  { name: 'Apr', value: 800 },
  { name: 'May', value: 500 }
];

const AnimatedLineChart = () => {
  return (
    <div >
      <LineChart 
        width={600} 
        height={300} 
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid 
          strokeDasharray="3 3" 
          vertical={false}
          stroke="rgba(255,255,255,0.1)"
        />
        <XAxis 
          dataKey="name" 
          stroke="#fff"
          tick={{ fill: '#fff' }}
        />
        <YAxis 
          stroke="#fff"
          tick={{ fill: '#fff' }}
          axisLine={false}
        />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#263238',
            border: 'none',
            color: '#fff'
          }}
        />
        <Legend 
          wrapperStyle={{ color: '#fff' }}
        />
        <Line 
          type="monotone" 
          dataKey="value" 
          stroke="#64b5f6"
          strokeWidth={2}
          dot={{ fill: '#64b5f6' }}
          animationDuration={2000}
          animationBegin={0}
          animationEasing="ease-in-out"
        />
      </LineChart>
    </div>
  );
};

export default AnimatedLineChart;