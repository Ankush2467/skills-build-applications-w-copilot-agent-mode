import React, { useState, useEffect } from 'react';

const Users = () => {
  const [data, setData] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const baseUrl = codespace
    ? `https://${codespace}-8000.app.github.dev`
    : 'http://localhost:8000';
  const url = `${baseUrl}/api/users/`;

  useEffect(() => {
    console.log('Fetching users from', url);
    fetch(url)
      .then((res) => res.json())
      .then((json) => {
        console.log('Users response', json);
        const items = json && json.results ? json.results : json;
        setData(items);
      })
      .catch((err) => console.error('Error fetching users', err));
  }, [url]);

  const generateDummy = () => {
    const headers = ['id', 'username', 'email'];
    const rows = [];
    for (let i = 1; i <= 5; i++) {
      rows.push({ id: i, username: `user${i}`, email: `user${i}@example.com` });
    }
    return { headers, rows };
  };

  const renderTable = (items) => {
    if (!items || items.length === 0) {
      const { headers, rows } = generateDummy();
      return (
        <table className="table table-striped">
          <thead>
            <tr>
              {headers.map((h) => (
                <th key={h}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={idx}>
                {headers.map((h) => (
                  <td key={h}>{String(row[h])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
    const headers = Object.keys(items[0]);
    return (
      <table className="table table-striped">
        <thead>
          <tr>
            {headers.map((h) => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((row, idx) => (
            <tr key={idx}>
              {headers.map((h) => (
                <td key={h}>{String(row[h])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="container mt-4">
      <h2 className="h3">Users</h2>
      {renderTable(data)}
    </div>
  );
};

export default Users;
