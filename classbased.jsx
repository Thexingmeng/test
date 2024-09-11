import React, { useState, useEffect } from 'react';

interface User {
  name: string;
  email: string;
}

interface UserDataProps {
  userId: string;
}

const UserData: React.FC<UserDataProps> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  const [seconds, setSeconds] = useState<number>(0);

  useEffect(() => {
    // 定义获取用户数据的函数
    const fetchUserData = async () => {
      try {
        const response = await fetch(`https://secret.url/user/${userId}`);
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error('获取用户数据时出错:', error);
      }
    };

    // 调用获取数据的函数
    fetchUserData();

    // 启动定时器
    const intervalId = setInterval(() => {
      setSeconds(prevSeconds => prevSeconds + 1);
    }, 1000);

    // 清理函数
    return () => {
      clearInterval(intervalId);
    };
  }, [userId]); // 当 userId 改变时重新获取数据

  return (
    <div>
      <h1>用户数据组件</h1>
      {user ? (
        <div>
          <p>姓名: {user.name}</p>
          <p>邮箱: {user.email}</p>
        </div>
      ) : (
        <p>正在加载用户数据...</p>
      )}
      <p>计时器: {seconds} 秒</p>
    </div>
  );
};

export default UserData;
