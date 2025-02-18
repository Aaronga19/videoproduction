import { Scroll, Calendar, DollarSign, ShieldCheck, Scale } from "lucide-react"

interface Props {
  nombre_cliente: string
}

export default function Contract({ nombre_cliente }: Props) {
  return (
    <div className="min-h-screen bg-amber-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto bg-white shadow-xl rounded-lg overflow-hidden">
        <div className="bg-amber-800 px-6 py-4">
          <h1 className="text-3xl font-bold text-amber-50 text-center">
            CONTRATO DE ARRENDAMIENTO DE EQUIPO AUDIOVISUAL
          </h1>
        </div>

        <div className="p-6 space-y-8">
          <div className="flex items-center justify-between">
            <span className="text-amber-900">Fecha de celebración:</span>
            <span className="font-semibold text-amber-900">[Fecha]</span>
          </div>

          <section className="space-y-4">
            <h2 className="text-2xl font-bold text-amber-800 flex items-center">
              <Scroll className="mr-2" /> PARTES CONTRATANTES
            </h2>
            <div className="bg-amber-100 p-4 rounded-lg space-y-2">
              <p>
                <strong className="text-amber-800">ARRENDADOR:</strong> [Nombre de la Empresa Arrendadora], con
                domicilio en [Dirección del Arrendador]
              </p>
              <p>
                <strong className="text-amber-800">ARRENDATARIO:</strong> {nombre_cliente}, con domicilio en [Dirección
                del Arrendatario]
              </p>
            </div>
          </section>

          <section className="space-y-6">
            <h2 className="text-2xl font-bold text-amber-800">CLÁUSULAS</h2>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800">PRIMERA: OBJETO DEL CONTRATO</h3>
              <p className="text-amber-900">
                El Arrendador da en arrendamiento al Arrendatario el siguiente equipo audiovisual:
              </p>
              <ul className="list-disc list-inside space-y-2 pl-4 text-amber-900">
                <li>
                  <strong>Cámaras:</strong> [Modelos y características específicas]
                </li>
                <li>
                  <strong>Luces:</strong> [Modelos y características específicas]
                </li>
                <li>
                  <strong>Ópticos:</strong> [Modelos y características específicas]
                </li>
              </ul>
              <p className="italic text-amber-700">
                El equipo se entrega en perfecto estado de funcionamiento y conservación, situación que el Arrendatario
                declara conocer y aceptar.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800 flex items-center">
                <Calendar className="mr-2" /> SEGUNDA: DURACIÓN DEL CONTRATO
              </h3>
              <p className="text-amber-900">
                El presente contrato tendrá una vigencia desde el día{" "}
                <span className="font-semibold">[Fecha de Inicio]</span> hasta el día{" "}
                <span className="font-semibold">[Fecha de Finalización]</span>.
              </p>
              <p className="italic text-amber-700">
                El Arrendatario se obliga a devolver el equipo en la fecha de finalización, salvo acuerdo expreso entre
                las partes para una prórroga.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800 flex items-center">
                <DollarSign className="mr-2" /> TERCERA: PRECIO Y FORMA DE PAGO
              </h3>
              <p className="text-amber-900">El Arrendatario se compromete a pagar al Arrendador:</p>
              <ul className="list-disc list-inside space-y-2 pl-4 text-amber-900">
                <li>
                  Precio total del arrendamiento: <span className="font-semibold">[Monto Total]</span>
                </li>
                <li>
                  Depósito en garantía: <span className="font-semibold">[Monto del Depósito]</span>
                </li>
              </ul>
              <p className="italic text-amber-700">
                Ambos montos deberán ser abonados en su totalidad antes de la entrega del equipo.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800 flex items-center">
                <ShieldCheck className="mr-2" /> CUARTA: DEPÓSITO EN GARANTÍA
              </h3>
              <p className="text-amber-900">
                El depósito en garantía será devuelto al Arrendatario una vez verificado que el equipo ha sido devuelto
                en las mismas condiciones en que fue entregado.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800">QUINTA: OBLIGACIONES DEL ARRENDATARIO</h3>
              <ul className="list-disc list-inside space-y-2 pl-4 text-amber-900">
                <li>
                  Utilizar el equipo de forma adecuada y conforme a las instrucciones proporcionadas por el Arrendador.
                </li>
                <li>
                  No realizar modificaciones, reparaciones o alteraciones al equipo sin la autorización previa y por
                  escrito del Arrendador.
                </li>
                <li>Devolver el equipo en las mismas condiciones en que fue recibido.</li>
                <li>
                  Asumir la responsabilidad total por la pérdida o daño del equipo durante el período de arrendamiento.
                </li>
              </ul>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800">SEXTA: RESPONSABILIDAD Y SEGURO</h3>
              <p className="text-amber-900">
                El Arrendatario será responsable de cualquier daño, pérdida o robo del equipo durante el período de
                arrendamiento. Se recomienda que el Arrendatario contrate un seguro que cubra estos riesgos.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800">SÉPTIMA: INDEMNIZACIÓN</h3>
              <p className="text-amber-900">
                El Arrendatario se compromete a indemnizar y mantener indemne al Arrendador frente a cualquier
                reclamación.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800">OCTAVA: TERMINACIÓN ANTICIPADA</h3>
              <p className="text-amber-900">
                El Arrendador podrá rescindir el presente contrato de forma inmediata en caso de incumplimiento de
                cualquiera de las obligaciones asumidas por el Arrendatario.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-amber-800 flex items-center">
                <Scale className="mr-2" /> NOVENA: JURISDICCIÓN Y LEY APLICABLE
              </h3>
              <p className="text-amber-900">
                El presente contrato se regirá por las leyes de{" "}
                <span className="font-semibold">[Jurisdicción Correspondiente]</span>.
              </p>
            </div>
          </section>

          <section className="space-y-6">
            <h2 className="text-2xl font-bold text-amber-800">FIRMA DE LAS PARTES</h2>
            <p className="italic text-amber-700">
              En prueba de conformidad, las partes firman el presente contrato en dos ejemplares de un mismo tenor y a
              un solo efecto, en el lugar y fecha indicados.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-amber-300 p-4 rounded-lg bg-amber-50">
                <p>
                  <strong className="text-amber-800">EL ARRENDADOR:</strong> [Nombre del Representante Legal]
                </p>
                <p className="mt-4">Firma: __________</p>
                <p>Fecha: __________</p>
              </div>

              <div className="border border-amber-300 p-4 rounded-lg bg-amber-50">
                <p>
                  <strong className="text-amber-800">EL ARRENDATARIO:</strong> [Nombre del Cliente]
                </p>
                <p className="mt-4">Firma: __________</p>
                <p>Fecha: __________</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

