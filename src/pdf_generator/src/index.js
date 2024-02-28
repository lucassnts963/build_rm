import puppeteer from 'puppeteer'
import { load } from 'cheerio'
import fs from 'fs'
import { program } from 'commander'
import path from 'path'
import dayjs from 'dayjs'

program
    .option('-d, --dataPath <file>', 'Arquivo de dados JSON')
    .option('-o, --output <file>', 'Arquivo de saída PDF')

program.parse(process.argv)

function buildMaterialsTable($, { data }) {
    const now = dayjs().format('YYYY-MM-DD_HH[hrs]mm[min]ss[seg]')

    const { company, date, expedition, draw, tag, local, destiny, aplication, rm, materials } = data

        $('#company').text(company)
        $('#contracted').text(company)
        $('#date').text(date)
        $('#expedition_date').text(expedition)
        $('#draw').text(draw)
        $('#tag').text(tag)
        $('#local').text(local)
        $('#destiny').text(destiny)
        $('#aplication').text(aplication)
        $('#request_number').text(rm)
        


        materials.forEach(item => {
            const tr = `
                <tr class="${ item.status }">
                    <td>${ item.code }</td>
                    <td>${ item.description }</td>
                    <td>${ item.dn }</td>
                    <td></td>
                    <td>${ item.quantity_requested }</td>
                    <td>${ item.quantity_required }</td>
                    <td>${ item.unit }</td>
                </tr>
            `

            $('#materials').append(tr)
        })

        const filename = `${rm}_${now}.pdf`.replace(' ', '_').replace('|', '_')

        return filename
}

async function start () {
    
    try {
        const cwd = process.cwd()

        const { dataPath, output } = program.opts()

        if (!dataPath || !output) {
            console.error('Por favor, informe todos os parâmentros.')
            return
        }

        const browser = await puppeteer.launch()
        const page = await browser.newPage()

        const templatePath = path.resolve(cwd, 'src', 'pdf_generator', 'src', 'template.html')
        const stylesPath = path.resolve(cwd, 'src', 'pdf_generator', 'src', 'styles.css')

        const htmlContent = fs.readFileSync(templatePath, 'utf-8')
        const jsonString = fs.readFileSync(dataPath, 'utf8')

        const data = JSON.parse(jsonString)

        const $ = load(htmlContent)

        const filepath = path.resolve(output, buildMaterialsTable($, { data }))

        const html = $.html()

        console.log(`Gerando PDF a partir de ${templatePath} para ${output}`)

        await page.setContent(html)
        await page.addStyleTag({ path: stylesPath })

        await page.pdf({ path: filepath, format: 'A4', landscape: true, preferCSSPageSize: true, printBackground: true })

        console.log(`PDF gerado com sucesso em ${filepath}`)

        await browser.close()
    } catch (error) {
        console.error('Ocorreu um erro:', error)
    }
}

start()
