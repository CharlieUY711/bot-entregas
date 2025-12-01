import React, { useState } from 'react';

interface Direccion {
  id: number;
  calle: string;
  numero: string;
  ciudad: string;
  codigoPostal: string;
  esPredeterminada: boolean;
}

interface Mensaje {
  id: number;
  texto: string;
  fecha: string;
  tipo: 'info' | 'success' | 'warning' | 'error';
}

const Perfil: React.FC = () => {
  const [entidadSeleccionada, setEntidadSeleccionada] = useState<string>('');
  const [direcciones] = useState<Direccion[]>([
    {
      id: 1,
      calle: 'Av. Principal',
      numero: '123',
      ciudad: 'Buenos Aires',
      codigoPostal: '1000',
      esPredeterminada: true,
    },
    {
      id: 2,
      calle: 'Calle Secundaria',
      numero: '456',
      ciudad: 'Buenos Aires',
      codigoPostal: '1001',
      esPredeterminada: false,
    },
    {
      id: 3,
      calle: 'Av. Terciaria',
      numero: '789',
      ciudad: 'Buenos Aires',
      codigoPostal: '1002',
      esPredeterminada: false,
    },
  ]);

  const [mensajes] = useState<Mensaje[]>([
    { id: 1, texto: 'Bienvenido al sistema', fecha: '2024-01-15 10:30', tipo: 'info' },
    { id: 2, texto: 'Perfil actualizado correctamente', fecha: '2024-01-14 15:20', tipo: 'success' },
    { id: 3, texto: 'Nueva dirección agregada', fecha: '2024-01-13 09:15', tipo: 'info' },
  ]);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Cabecera */}
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Perfil</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-gray-700">253-ENT-12345</span>
          <button className="rounded-lg bg-purple-200 px-4 py-2 text-sm font-medium text-purple-800 hover:bg-purple-300">
            Rastrear
          </button>
          <button className="rounded-lg p-2 text-gray-600 hover:bg-gray-200">
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
          <button className="rounded-lg p-2 text-gray-600 hover:bg-gray-200">
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </button>
        </div>
      </div>

      {/* Grid de Cards */}
      <div className="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Card #1: Foto, Nombre, Email, Selector de Entidades */}
        <div className="rounded-xl bg-white p-6 shadow-md">
          <div className="mb-4 flex items-center gap-4">
            <div className="h-20 w-20 overflow-hidden rounded-full bg-gray-200">
              <img
                src="https://via.placeholder.com/80"
                alt="Foto de perfil"
                className="h-full w-full object-cover"
              />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold text-gray-900">Nombre de Usuario</h2>
              <p className="text-sm text-gray-600">usuario@ejemplo.com</p>
            </div>
          </div>
          
          {/* Campo transparente de 1.2 cm (aproximadamente 45px) */}
          <div className="mb-4 h-[45px] rounded-lg bg-transparent border-2 border-dashed border-gray-300"></div>
          
          {/* Selector de Entidades */}
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">
              Seleccionar Entidad
            </label>
            <select
              value={entidadSeleccionada}
              onChange={(e) => setEntidadSeleccionada(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
            >
              <option value="">Seleccione una entidad</option>
              <option value="entidad1">Entidad 1</option>
              <option value="entidad2">Entidad 2</option>
              <option value="entidad3">Entidad 3</option>
            </select>
          </div>
        </div>

        {/* Card #2: Datos Personales */}
        <div className="rounded-xl bg-white p-6 shadow-md">
          <h3 className="mb-4 text-lg font-semibold text-gray-900">Datos Personales</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700">Nombre Completo</label>
              <input
                type="text"
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
                defaultValue="Juan Pérez"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Teléfono</label>
              <input
                type="tel"
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
                defaultValue="+54 11 1234-5678"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">DNI</label>
              <input
                type="text"
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
                defaultValue="12.345.678"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Fecha de Nacimiento</label>
              <input
                type="date"
                className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
                defaultValue="1990-01-01"
              />
            </div>
          </div>
        </div>

        {/* Card #3: Direcciones */}
        <div className="rounded-xl bg-white p-6 shadow-md">
          <h3 className="mb-4 text-lg font-semibold text-gray-900">Direcciones</h3>
          <div className="space-y-3">
            {direcciones.map((direccion, index) => (
              <div
                key={direccion.id}
                className={`rounded-lg border-2 p-4 ${
                  direccion.esPredeterminada
                    ? 'border-purple-500 bg-purple-50'
                    : 'border-gray-200 bg-white'
                }`}
                style={{
                  marginLeft: direccion.esPredeterminada ? '0' : `${(index - 1) * 20}px`,
                }}
              >
                {direccion.esPredeterminada && (
                  <span className="mb-2 inline-block rounded-full bg-purple-500 px-2 py-1 text-xs font-medium text-white">
                    Predeterminada
                  </span>
                )}
                <p className="font-medium text-gray-900">
                  {direccion.calle} {direccion.numero}
                </p>
                <p className="text-sm text-gray-600">
                  {direccion.ciudad}, CP {direccion.codigoPostal}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Card #4: Monitor con Mensajes */}
        <div className="rounded-xl bg-gray-900 p-6 shadow-md">
          <div className="mb-4 flex items-center gap-2">
            <div className="flex gap-1">
              <div className="h-3 w-3 rounded-full bg-red-500"></div>
              <div className="h-3 w-3 rounded-full bg-yellow-500"></div>
              <div className="h-3 w-3 rounded-full bg-green-500"></div>
            </div>
            <span className="ml-2 text-xs text-gray-400">Mensajes del Sistema</span>
          </div>
          <div className="h-64 space-y-2 overflow-y-auto rounded-lg bg-black p-4 font-mono text-sm">
            {mensajes.map((mensaje) => (
              <div
                key={mensaje.id}
                className={`rounded p-2 ${
                  mensaje.tipo === 'info'
                    ? 'bg-blue-900 text-blue-200'
                    : mensaje.tipo === 'success'
                    ? 'bg-green-900 text-green-200'
                    : mensaje.tipo === 'warning'
                    ? 'bg-yellow-900 text-yellow-200'
                    : 'bg-red-900 text-red-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">[{mensaje.fecha}]</span>
                  <span className="text-xs uppercase">{mensaje.tipo}</span>
                </div>
                <p className="mt-1">{mensaje.texto}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Buscador */}
      <div className="mb-6">
        <div className="relative">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <svg
              className="h-5 w-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <input
            type="text"
            placeholder="Buscar direcciones..."
            className="w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-200"
          />
        </div>
      </div>

      {/* Botones de Acción */}
      <div className="flex gap-4">
        <button className="flex items-center gap-2 rounded-lg bg-green-500 px-6 py-3 font-medium text-white transition-colors hover:bg-green-600">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          Crear
        </button>
        <button className="flex items-center gap-2 rounded-lg bg-green-500 px-6 py-3 font-medium text-white transition-colors hover:bg-green-600">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
            />
          </svg>
          Editar
        </button>
        <button className="flex items-center gap-2 rounded-lg bg-green-500 px-6 py-3 font-medium text-white transition-colors hover:bg-green-600">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
          Grabar modificaciones
        </button>
      </div>
    </div>
  );
};

export default Perfil;
