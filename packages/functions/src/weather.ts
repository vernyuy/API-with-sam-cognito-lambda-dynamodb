interface Weather {
    weatherId: string;
    weather: string;
    createdAt: number;
    town: string;
  }
  
  const weather: { [key: string]: Weather } = {
    id1: {
      weatherId: "id1",
      weather: "user1",
      createdAt: Date.now(),
      town: "Hello World!",
    },
    id2: {
      weatherId: "id2",
      weather: "user2",
      createdAt: Date.now() - 10000,
      town: "yaounde",
    },
  };
  
  export default weather;